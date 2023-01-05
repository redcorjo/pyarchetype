#!/bin/bash

BASE_DIR=$(dirname -- "$0")/..
TWINE_CONFIG=$(dirname -- "$0")/../.pypirc

source ${BASE_DIR}/.venv/bin/activate

twine upload dist/* --config-file $TWINE_CONFIG 

exit