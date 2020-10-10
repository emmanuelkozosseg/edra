#!/bin/bash
set -ex

if [[ ! -d songs ]]; then
    echo "ERROR: This script needs to run in the repository's root directory." >&2
    exit 1
fi

# Parse flags
[[ "$*" == *--create-opensong-package* ]] && CREATE_OPENSONG_PACKAGE=1

# Done this way to avoid having to install 'zip'. It's equivalent to:
# cd dist/Emmánuel/
# zip -r -9 ../opensong.zip .
# cd ../..
function zip() {
    local rootdir=$1  # Path to the directory whose contents we want to zip
    local basedir=$2  # Zip only the contents of this directory within the root
    local targetfile=$3  # Path to the target file, WITHOUT FILE EXTENSION
    python3 -c "import shutil; shutil.make_archive(base_name='$targetfile', format='zip', root_dir='$rootdir', base_dir='$basedir')"
}
function unzip() {
    local zipfile=$1
    local targetdir=$2
    python3 -c "import shutil; shutil.unpack_archive(filename='$zipfile', extract_dir='$targetdir')"
}

# Cleanup and preparation
rm -rf dist/
mkdir dist/

# Conversions
python3 bin/convert.py opensong --from-dir songs/ --to-dir dist/Emmánuel/
python3 bin/convert.py emmet-json --from-dir songs/ --to dist/emmet.json
python3 bin/convert.py diatar --from-dir songs/ --to dist/emmanuel.dtx
python3 bin/convert.py pdf --from-dir songs/ --to dist/emmet_offline.pdf

# Zip up OpenSong files
zip "dist" "Emmánuel" "dist/opensong-enekek"

# Download the portable OpenSong, patch song files into it, and create the OpenSong package
# (only when explicitly requested)
if [[ $CREATE_OPENSONG_PACKAGE ]]; then
    wget -P dist/ "https://bitbucket.org/eckerg/emmert/downloads/opensong-skeleton.zip"
    unzip dist/opensong-skeleton.zip dist/
    mv dist/Emmánuel/ "dist/OpenSong/OpenSong Data/Songs/"
    zip "dist" "OpenSong" "dist/opensong-csomag"
    rm -rf dist/OpenSong/ dist/opensong-skeleton.zip
else
    echo "Not creating a portable OpenSong package. Pass --create-opensong-package to enable this."
fi

# Upload files to Bitbucket
if [[ $BB_AUTH_STRING ]]; then
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/opensong-enekek.zip"
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/opensong-csomag.zip"
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/emmet.json"
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/emmanuel.dtx"
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/emmet_offline.pdf"
else
    echo "No BB_AUTH_STRING variable found, not deploying artifacts."
fi
