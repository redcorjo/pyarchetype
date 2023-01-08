#!/bin/bash

BASE_DIR=$(dirname $0)/..
TWINE_CONFIG=$(dirname $0)/../.pypirc
PYTHON=python3.7
PACKAGE=pyarchetype

cd ${BASE_DIR}

echo Reinstall module
python -m pip install --upgrade --force-reinstall dist/${PACKAGE}*whl

echo Run tests
python tests/test_cli.py

pyarchetype -h

echo "Upload to pypi"
if test -e ${TWINE_CONFIG}
then
    chmod 600 ${TWINE_CONFIG}
    twine upload dist/${PACKAGE}* --config-file ${TWINE_CONFIG} 
else
    twine upload dist/*
fi

exit