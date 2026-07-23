# Chocolatey package

Source for the `glabels-qt` package on the
[Chocolatey Community Repository](https://community.chocolatey.org/packages/glabels-qt).

> **Why not the id `glabels`?** It is taken. An unrelated 2020 submission holds it; its only
> version was rejected in April 2020 and it has been dormant since. Pushing to an id owned by
> another account returns a bare `403 Forbidden`, which is easy to mistake for a bad API key.
> Reclaiming it would mean going through Chocolatey's package triage process with the site
> admins; `glabels-qt` matches the upstream project's own name and needed no waiting.

The package **downloads** the installer from this repository's GitHub release and verifies
it against the SHA-256 in [`tools/chocolateyinstall.ps1`](tools/chocolateyinstall.ps1);
nothing is embedded in the `.nupkg`.

## Why Chocolatey fits where Scoop did not

Chocolatey's model is third parties maintaining packages for other people's software — its
validator raises a *note* when `owners` matches `authors`, i.e. it expects them to differ.
So `authors` credits the gLabels authors and `owners` is the packager. There is also no
"latest stable only" rule, which is what [blocks the Scoop submission](../scoop/).

## Publishing a new version

1. Update `version`, the release URL and `checksum64` in
   [`glabels-qt.nuspec`](glabels-qt.nuspec) and [`tools/chocolateyinstall.ps1`](tools/chocolateyinstall.ps1),
   and the URL, checksum and commit in [`tools/VERIFICATION.txt`](tools/VERIFICATION.txt).
   The checksum is published as `SHA256SUMS.txt` on every release.
2. Push, which runs [`chocolatey.yml`](../.github/workflows/chocolatey.yml). It packs the
   package, installs it from a local source on a clean runner, checks the registry entry and
   the installed tree, and uninstalls again. A red run means do not publish.
3. Run the **Publish to Chocolatey** workflow and type `PUBLISH` in the confirm field. It
   re-packs, re-runs the install/verify/uninstall test, and only then pushes.
4. Expect moderation. New packages are reviewed by a human and a package's first submission
   usually gets comments.

Uploading a `.nupkg` through the website **is no longer supported** — the repository
retired it in favour of `choco push`, which is why publishing goes through the workflow.
That needs a repository secret:

| | |
|:--|:--|
| Secret | `CHOCO_API_KEY` |
| Where to get it | <https://community.chocolatey.org/account> |
| Where to put it | Settings → Secrets and variables → Actions → New repository secret |

Publishing is a separate, manual workflow rather than part of the build because a version
number, once pushed, can never be reused — even if the package is later unlisted.

## Things that will silently break

* `softwareName` in `chocolateyinstall.ps1` is `gLabels 4*`, matched against the installer's
  `DisplayName` (`gLabels 4 Label Designer`). If the display name changes, Chocolatey's
  auto-uninstaller stops finding it. The workflow asserts this pattern still matches.
* The `iconUrl` must not be a `raw.githubusercontent.com` URL — that is a hard validation
  error. It uses jsDelivr, pinned to a commit so the icon cannot change under us.
