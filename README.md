<div align="center">

# gLabels 4 for Windows

**Ready-to-run Windows builds of [gLabels 4](https://github.com/j-evins/glabels-qt) — the free label and business-card designer.**

[![Build gLabels for Windows](https://github.com/ibsorn/glabels-windows/actions/workflows/build-windows.yml/badge.svg)](https://github.com/ibsorn/glabels-windows/actions/workflows/build-windows.yml)
[![Latest release](https://img.shields.io/github/v/release/ibsorn/glabels-windows?label=latest%20build)](https://github.com/ibsorn/glabels-windows/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/ibsorn/glabels-windows/total?label=downloads)](https://github.com/ibsorn/glabels-windows/releases)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

### [⬇️ Download the latest build](https://github.com/ibsorn/glabels-windows/releases/latest)

</div>

---

## What is this?

Upstream gLabels 4 (`glabels-qt`) is cross-platform and builds fine on Windows, but the
project does not currently ship Windows binaries — you are expected to install Visual
Studio, Qt, CMake and a handful of libraries and build it yourself.

This repository does that for you, in public, on GitHub's own runners. Every release is
produced by [one workflow file](.github/workflows/build-windows.yml) from unmodified
upstream sources, so you can read exactly how the binary you downloaded was made — and
reproduce it yourself by forking this repo and pressing *Run workflow*.

## Download

Grab the files from the [**latest release**](https://github.com/ibsorn/glabels-windows/releases/latest):

| File | Use it if… |
|:--|:--|
| `gLabels-<version>-win64-setup.exe` | You want a normal installation: Start-menu and desktop shortcuts, `.glabels` file association, clean uninstaller. |
| `gLabels-<version>-win64-portable.zip` | You want to run it from a USB stick or without installing anything. Unzip anywhere and run `bin\glabels-qt.exe`. |
| `SHA256SUMS.txt` | You want to verify what you downloaded. |

**Requirements:** 64-bit Windows 10 or 11. Nothing else — Qt and the C runtime are bundled.

### Package managers

**winget** — submitted as `ibsorn.gLabels`, in review at
[winget-pkgs#406476](https://github.com/microsoft/winget-pkgs/pull/406476). Once merged,
`winget install ibsorn.gLabels` will work. Not before.

**Scoop** — [not eligible yet](scoop/). The Extras bucket requires the *latest stable
version* of a package, and gLabels 4 has no stable release. The manifest is written and
ready in [`scoop/`](scoop/) for the day upstream tags 4.0.

<details>
<summary>Verifying a download</summary>

```powershell
Get-FileHash .\gLabels-3.99-master639-win64-setup.exe -Algorithm SHA256
```

Compare the result with the matching line in `SHA256SUMS.txt`.
</details>

<details>
<summary>“Windows protected your PC”</summary>

The installer is not code-signed (a certificate costs several hundred euros a year), so
SmartScreen shows a warning the first time. Choose **More info → Run anyway**, or use the
portable ZIP instead. The SHA-256 sums above, the build log of every release, and the
workflow file are all public so you can check what you are running.
</details>

## What's inside

| | |
|:--|:--|
| Application | gLabels 4 development snapshot (`glabels-qt`, `master`) |
| Toolchain | MSVC 2022, 64-bit, Release |
| Qt | 6.8.x LTS, deployed with `windeployqt` |
| Barcodes | built-in *glbarcode++*, **zint** and **libqrencode** |
| Compressed projects | zlib |
| Extras | full upstream template database (35+ vendors) and all translations |
| Also included | `glabels-batch-qt.exe`, the command-line renderer |

Every build runs the upstream unit tests plus a smoke test that renders a PDF from the
*packaged* tree, so a release can only be published if the deployed binaries actually run.

## Status

gLabels 4 is still under active development upstream — there is no final 4.0 release yet.
What you get here are snapshots of the `master` branch, rebuilt weekly and whenever
upstream changes are picked up. They are usable, but treat them as pre-release software
and keep backups of your projects.

## Building it yourself

Fork this repository and use **Actions → Build gLabels for Windows → Run workflow**. You
can point it at any upstream branch, tag or commit, and optionally have it publish a
release in your own fork. Nothing besides a GitHub account is required.

Locally, follow the
[upstream Windows build instructions](https://github.com/j-evins/glabels-qt/blob/master/docs/BUILD-INSTRUCTIONS-WINDOWS.md).

Note that the *process* is reproducible, not the bytes: MSVC and NSIS embed timestamps, so
rebuilding the same commit gives you a working, equivalent binary with a different SHA-256.
The published sums identify a specific release, they are not a build fingerprint.

Any local fixes needed to build a given upstream revision live in [`patches/`](patches/)
as plain `git apply` patches, each with a header explaining why it exists and what would
make it removable. The packaging metadata (installer name, icons, file association) lives
in [`packaging/`](packaging/). No gLabels source code is modified beyond those patches.

## Bugs

* **Something wrong with the installer, packaging, or a missing DLL** → [open an issue here](https://github.com/ibsorn/glabels-windows/issues).
* **Something wrong with gLabels itself** → report it [upstream](https://github.com/j-evins/glabels-qt/issues), where the people who can fix it are.

## Credits and licence

gLabels is written by **Jaye Evins** and contributors. This repository contains no gLabels
source code — only build automation — but the binaries it produces are gLabels and are
distributed under the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0)
like the original. The corresponding source for every release is the upstream commit named
in the release notes.

This is an **unofficial community build** and is not endorsed by or affiliated with the
gLabels project.
