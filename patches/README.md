# Patches

Any `*.patch` file dropped in this directory is applied to the upstream `glabels-qt`
checkout with `git apply`, in alphabetical order, before the build is configured.

Use this for fixes that are needed to build a given upstream revision on Windows and that
have not landed upstream yet. Keep each patch minimal, name it `NNNN-short-description.patch`,
and add a comment at the top explaining why it exists and what makes it removable.

This directory is currently empty on purpose — upstream builds cleanly with MSVC.
