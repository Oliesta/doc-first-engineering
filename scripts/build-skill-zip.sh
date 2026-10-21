#!/usr/bin/env sh
# Rebuilds dist/doc-first-engineering.zip from the skill folder.
# Run from the repository root after changing the skill.
set -eu
cd plugins/doc-first-engineering/skills
rm -f ../../../dist/doc-first-engineering.zip
zip -rq ../../../dist/doc-first-engineering.zip doc-first-engineering
echo "Built dist/doc-first-engineering.zip"
