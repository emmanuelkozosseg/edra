#!/bin/bash
set -ex

if [[ ! -d songs ]]; then
    echo "ERROR: This script needs to run in the repository's root directory." >&2
    exit 1
fi

# Prepare Python
python3 -m venv .venv/
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Cleanup and preparation
rm -rf dist/
mkdir dist/

# Find current commit's date
COMMIT_DATE=$(git show -s --format=%cd --date=format:%Y.%m.%d.)

# Conversions
python bin/convert.py opensong --from-dir songs/ --to-dir dist/Emmánuel/
python bin/convert.py emmet-json --from-dir songs/ --to dist/emmet.json --version $COMMIT_DATE
python bin/convert.py diatar --from-dir songs/ --to dist/emmanuel.dtx
python bin/convert.py pdf --from-dir songs/ --to dist/emmet_offline.pdf

cd dist/

# Zip up OpenSong song files
zip -r opensong-enekek.zip Emmánuel

# Patch song files into the portable OpenSong package
unzip ../opensong-skeleton.zip
mv Emmánuel/ "OpenSong/OpenSong Data/Songs/"
zip -r opensong-csomag.zip OpenSong
rm -rf OpenSong/ opensong-skeleton.zip
