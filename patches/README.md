# Patches

Any `*.patch` file dropped in this directory is applied to the upstream `glabels-qt`
checkout with `git apply`, in alphabetical order, before the build is configured.

Use this for fixes that are needed to build a given upstream revision on Windows and that
have not landed upstream yet. Keep each patch minimal, name it `NNNN-short-description.patch`,
and add a comment at the top explaining why it exists and what makes it removable.

## Current patches

| Patch | Why |
|:--|:--|
| `0001-no-lupdate-during-build.patch` | The upstream build regenerates the two C-locale `.ts` files with `lupdate` on every build. Qt 6's `lupdate` is the clang-based parser and needs `libclang.dll`, which the `qttools` archive fetched by aqtinstall does not contain, so it dies with `STATUS_DLL_NOT_FOUND`. Both `.ts` files are committed upstream, so the patch compiles them with `lrelease` instead — which is all a packaging build needs. |
