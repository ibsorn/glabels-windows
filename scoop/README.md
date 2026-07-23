# Scoop manifest

[`glabels.json`](glabels.json) is the manifest submitted to the
[Extras bucket](https://github.com/ScoopInstaller/Extras), so that
`scoop install extras/glabels` works.

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
