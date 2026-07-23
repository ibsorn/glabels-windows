# Scoop manifest

> **Not submitted — blocked until gLabels 4.0 is released.**
>
> The Extras bucket's [package criteria](https://github.com/ScoopInstaller/Extras/blob/master/.github/ISSUE_TEMPLATE/package-request.yml)
> require the *latest stable version*, and every release here is a snapshot of upstream's
> `master` because gLabels 4 has no stable release yet. gLabels clears the bucket's other
> required bars easily — the upstream project has ~470 stars and the application ships in
> Debian, Fedora, Ubuntu and Arch — so this is purely a matter of waiting.
>
> A first attempt ([Extras#18371](https://github.com/ScoopInstaller/Extras/pull/18371)) was
> withdrawn once that criterion was checked. When upstream tags 4.0: open a package request
> issue **first** (the bucket requires one before a PR), refresh the version, URL, hash and
> `extract_dir` below, and resubmit.

[`glabels.json`](glabels.json) is the manifest for the
[Extras bucket](https://github.com/ScoopInstaller/Extras), so that
`scoop install extras/glabels` would work.

It installs the **portable ZIP**, not the installer — Scoop manages its own directories and
does not want a package writing to `Program Files` or the registry.

Two things to keep in mind when editing it:

* `extract_dir` must keep the archive's `bin/` + `share/` layout intact. gLabels finds its
  template database by walking up from the executable and looking for `../share/glabels-qt`,
  and it aborts at startup if that fails — flattening the archive would break it.
* `autoupdate.hash` reads the `SHA256SUMS.txt` published with every release, so new versions
  are picked up by Scoop's Excavator bot without a manual hash update. If the release ever
  stops publishing that file, this silently stops working.

Validate a change against Scoop's schema before submitting:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/ScoopInstaller/Scoop/master/schema.json -OutFile schema.json
# then check glabels.json against it, or run the bucket's own Scoop-Bucket.Tests.ps1
```
