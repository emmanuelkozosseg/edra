#!/bin/bash
set -ex

if [[ ! -d songs ]]; then
    echo "ERROR: This script needs to run in the repository's root directory." >&2
    exit 1
fi

rm -rf dist/
mkdir dist/

python3 bin/convert.py opensong --from-dir songs/ --to-dir dist/Emmánuel/
python3 bin/convert.py json --from-dir songs/ --to dist/songs.json
python3 bin/convert.py diatar --from-dir songs/ --to dist/emmanuel.dtx
python3 bin/convert.py pdf --from-dir songs/ --to dist/emmet_offline.pdf

# Done this way to avoid having to install 'zip'. It's equivalent to:
# cd dist/Emmánuel/
# zip -r -9 ../opensong.zip .
# cd ../..
python3 -c "import shutil; shutil.make_archive(base_name='dist/opensong-enekek', format='zip', root_dir='dist', base_dir='Emmánuel')"

if [[ $BB_AUTH_STRING ]]; then
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/opensong-enekek.zip"
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/songs.json"
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/emmanuel.dtx"
    curl -v -X POST "https://${BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/downloads" --form files=@"dist/emmet_offline.pdf"
else
    echo "No BB_AUTH_STRING variable found, not deploying artifacts."
fi
