#!/bin/bash

set -eu

BUILDROOT="docbuild"

pdoc --no-show-source -o "$BUILDROOT" chipchune

[ "$GH_PASSWORD" ] || exit 12

git clone -b gh-pages "https://zoomten:$GH_PASSWORD@github.com/$GITHUB_REPOSITORY.git" gh-pages

cp -R docbuild/* gh-pages/

cd gh-pages

git add *

if git diff --staged --quiet; then
  echo "$0: No changes to commit."
  exit 0
fi

if ! git config user.name; then
    git config user.name 'github-actions'
    git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
fi

git commit -a -m "CI: Update docs"
git push
