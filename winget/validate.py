#!/usr/bin/env python3
"""Validate a winget manifest set before opening a winget-pkgs pull request.

    python winget/validate.py winget/3.99.639

Checks every manifest in the directory against the official JSON schema for the
ManifestVersion it declares, then cross-checks the things winget requires to
agree across the set. Requires `pyyaml` and `jsonschema`.
"""
import base64
import datetime
import glob
import json
import os
import sys
import urllib.request

import jsonschema
import yaml

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".schemas")
REQUIRED_TYPES = {"version", "installer", "defaultLocale"}


def schema_for(manifest_type, manifest_version):
    """Fetch a schema from microsoft/winget-cli, caching it on disk."""
    name = f"manifest.{manifest_type}.{manifest_version}.json"
    cached = os.path.join(CACHE, name)
    if not os.path.exists(cached):
        os.makedirs(CACHE, exist_ok=True)
        url = (
            "https://api.github.com/repos/microsoft/winget-cli/contents/"
            f"schemas/JSON/manifests/v{manifest_version}/{name}"
        )
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            payload = json.load(r)
        with open(cached, "wb") as f:
            f.write(base64.b64decode(payload["content"]))
    with open(cached, encoding="utf-8") as f:
        return json.load(f)


def stringify_dates(node):
    """PyYAML parses an unquoted `2026-07-22` into a date object, which the
    schema then rejects as "not of type string". winget's own parser treats it
    as a string and merged manifests write it unquoted, so normalise here rather
    than making the manifest non-idiomatic."""
    if isinstance(node, dict):
        return {k: stringify_dates(v) for k, v in node.items()}
    if isinstance(node, list):
        return [stringify_dates(v) for v in node]
    if isinstance(node, (datetime.date, datetime.datetime)):
        return node.isoformat()
    return node


def main(directory):
    problems = 0
    docs = {}

    for path in sorted(glob.glob(os.path.join(directory, "*.yaml"))):
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            doc = stringify_dates(yaml.safe_load(f))
        mtype, mver = doc.get("ManifestType"), doc.get("ManifestVersion")
        if mtype is None or mver is None:
            print(f"FAIL {name}: ManifestType/ManifestVersion missing")
            problems += 1
            continue
        docs[mtype] = doc

        errors = sorted(
            jsonschema.Draft7Validator(schema_for(mtype, mver)).iter_errors(doc),
            key=lambda e: list(e.path),
        )
        if errors:
            problems += len(errors)
            print(f"FAIL {name}")
            for e in errors:
                print(f"       {'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}")
        else:
            print(f"OK   {name}  ({mtype}, schema {mver})")

    missing = REQUIRED_TYPES - set(docs)
    if missing:
        problems += 1
        print(f"FAIL missing manifest types: {sorted(missing)}")

    keys = {t: (d.get("PackageIdentifier"), d.get("PackageVersion")) for t, d in docs.items()}
    if len(set(keys.values())) > 1:
        problems += 1
        print(f"FAIL PackageIdentifier/PackageVersion disagree across manifests: {keys}")
    elif keys:
        print(f"OK   PackageIdentifier/PackageVersion consistent: {next(iter(keys.values()))}")

    default_locale = docs.get("version", {}).get("DefaultLocale")
    package_locale = docs.get("defaultLocale", {}).get("PackageLocale")
    if default_locale != package_locale:
        problems += 1
        print(f"FAIL DefaultLocale ({default_locale}) != PackageLocale ({package_locale})")
    else:
        print(f"OK   DefaultLocale matches PackageLocale: {default_locale}")

    print("\n" + ("ALL CHECKS PASSED" if not problems else f"{problems} PROBLEM(S)"))
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
