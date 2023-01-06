#!/bin/bash

BASE_DIR=$(dirname $0)/..
TWINE_CONFIG=$(dirname $0)/../.pypirc
PYTHON=python3.7
PACKAGE=pyarchetype

cd ${BASE_DIR}

echo "Upload to pypi"
if test -e ${TWINE_CONFIG}
then
    chmod 600 ${TWINE_CONFIG}
    twine upload dist/${PACKAGE}* --config-file ${TWINE_CONFIG} 
else
    twine upload dist/*
fi

python -m pip install --upgrade dist/${PACKAGE}*whl

pyarchetype -h

exit