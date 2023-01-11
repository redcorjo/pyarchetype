#!/bin/bash

BASE_DIR=$(dirname $0)/..
TWINE_CONFIG=$(dirname $0)/../.pypirc
PYTHON=python3.7
PACKAGE=pyarchetype

cd ${BASE_DIR}

echo "Cleanup old dist files"
test -e ${BASE_DIR}/dist/*.whl && rm ${BASE_DIR}/dist/* 

if ! test -e ${BASE_DIR}/.venv/bin/activate
then
    echo "Creating default virtual environment"
    ${PYTHON} -m venv .venv
    echo "Enable virtual environment"
    source ${BASE_DIR}/.venv/bin/activate
    python -m pip install --upgrade pip build twine
else
    echo "Enable virtual environment"
    source ${BASE_DIR}/.venv/bin/activate
fi

python -m build 2>/dev/null >/dev/null || python -m pip install --upgrade pip build

echo "Build"
python -m build

# echo "Upload to pypi"
# if test -e ${TWINE_CONFIG}
# then
#     chmod 600 ${TWINE_CONFIG}
#     twine upload dist/${PACKAGE}* --config-file ${TWINE_CONFIG} 
# else
#     twine upload dist/*
# fi

echo Reinstall module
python -m pip install --upgrade --force-reinstall dist/${PACKAGE}*whl

echo Run tests
python tests/test_cli.py

echo Run help
pyarchetype -h

exit