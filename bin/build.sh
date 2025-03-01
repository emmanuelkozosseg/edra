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
pip install -r requirements.txt

# Done this way to avoid having to install 'zip'. It's equivalent to:
# cd dist/Emmánuel/
# zip -r -9 ../opensong.zip .
# cd ../..
function zip() {
    local rootdir=$1  # Path to the directory whose contents we want to zip
    local basedir=$2  # Zip only the contents of this directory within the root
    local targetfile=$3  # Path to the target file, WITHOUT FILE EXTENSION
    python -c "import shutil; shutil.make_archive(base_name='$targetfile', format='zip', root_dir='$rootdir', base_dir='$basedir')"
}
function unzip() {
    local zipfile=$1
    local targetdir=$2
    python -c "import shutil; shutil.unpack_archive(filename='$zipfile', extract_dir='$targetdir')"
}

# Cleanup and preparation
rm -rf dist/
mkdir dist/

# Conversions
python bin/convert.py opensong --from-dir songs/ --to-dir dist/Emmánuel/
python bin/convert.py emmet-json --from-dir songs/ --to dist/emmet.json
python bin/convert.py diatar --from-dir songs/ --to dist/emmanuel.dtx
python bin/convert.py pdf --from-dir songs/ --to dist/emmet_offline.pdf

# Zip up OpenSong files
zip "dist" "Emmánuel" "dist/opensong-enekek"

# Patch song files into the portable OpenSong package
unzip opensong-skeleton.zip dist/
mv dist/Emmánuel/ "dist/OpenSong/OpenSong Data/Songs/"
zip "dist" "OpenSong" "dist/opensong-csomag"
rm -rf dist/OpenSong/ dist/opensong-skeleton.zip
