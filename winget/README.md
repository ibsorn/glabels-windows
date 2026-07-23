# winget manifests

Manifests for submitting a release to [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs),
so that `winget install glabels` works.

One directory per published version, laid out the way winget-pkgs expects. To submit,
copy the directory to `manifests/i/ibsorn/gLabels/<version>/` in a fork of winget-pkgs and
open a pull request.

## Conventions used here

| | |
|:--|:--|
| `PackageIdentifier` | `ibsorn.gLabels` — the publisher segment is the person who publishes *these binaries*, not the gLabels authors, because these are unofficial builds. |
| `PackageVersion` | Normalised to `3.99.<commit-count>` so winget can order versions. The snapshot string upstream uses (`3.99-master639`) is recorded as `AppsAndFeaturesEntries.DisplayVersion` instead. |
| `ProductCode` | `gLabels 4` — the uninstall registry subkey, which is `CPACK_PACKAGE_INSTALL_REGISTRY_KEY`. **Do not change it between versions**; winget correlates installed packages on it, so changing it would orphan every existing installation. |

## Validating before submitting

`validate.py` checks each manifest against the official JSON schema and cross-checks the
identifier, version and locale across the set:

```bash
pip install pyyaml jsonschema
python winget/validate.py winget/3.99.639
```

The schemas are fetched from `microsoft/winget-cli` and cached in `winget/.schemas/`.

The build workflow separately installs the packaged installer on a clean runner, asserts
the registry entry matches what these manifests claim, and uninstalls again — so a wrong
`ProductCode` or `DisplayVersion` fails the build rather than reaching winget.
