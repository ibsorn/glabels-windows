# Chocolatey package

Source for the `glabels` package on the
[Chocolatey Community Repository](https://community.chocolatey.org/packages/glabels).

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
   [`glabels.nuspec`](glabels.nuspec) and [`tools/chocolateyinstall.ps1`](tools/chocolateyinstall.ps1),
   and the URL, checksum and commit in [`tools/VERIFICATION.txt`](tools/VERIFICATION.txt).
   The checksum is published as `SHA256SUMS.txt` on every release.
2. Push, which runs [`chocolatey.yml`](../.github/workflows/chocolatey.yml). It packs the
   package, installs it from a local source on a clean runner, checks the registry entry and
   the installed tree, and uninstalls again. A red run means do not publish.
3. Download the `chocolatey-package` artifact from that run and upload the `.nupkg` at
   <https://push.chocolatey.org/>, or `choco push <file>.nupkg --source https://push.chocolatey.org/`
   with your API key.
4. Expect moderation. New packages are reviewed by a human and the first submission of a
   package usually gets comments.

Pushing is not automated: it needs an API key that should not live in this repository's
secrets for a package that is moderated anyway.

## Things that will silently break

* `softwareName` in `chocolateyinstall.ps1` is `gLabels 4*`, matched against the installer's
  `DisplayName` (`gLabels 4 Label Designer`). If the display name changes, Chocolatey's
  auto-uninstaller stops finding it. The workflow asserts this pattern still matches.
* The `iconUrl` must not be a `raw.githubusercontent.com` URL — that is a hard validation
  error. It uses jsDelivr, pinned to a commit so the icon cannot change under us.
