#!/bin/bash

# ----------------------------------
# Colors
# ----------------------------------
NOCOLOR='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
Purple='\033[0;35m'

eval "$(conda shell.bash hook)"

if { conda env list | grep 'rte'; } >/dev/null 2>&1; then
    echo -e "conda env 'rte' : ${GREEN}found${NOCOLOR}"
else
    echo -e "conda env 'rte' : ${RED}not found${NOCOLOR}"
    echo -e "conda env 'rte' : ${GREEN}creating${NOCOLOR}"
    conda env create -n rte -f environment.yml
    echo -e "conda env 'rte' : ${GREEN}created${NOCOLOR}"
fi

echo -e "conda env 'rte' : ${GREEN}activate${NOCOLOR}"
conda activate rte

echo -e "Running pycln"
pycln ./* main.py -s -a

echo -e "Running isort"
isort ./* main.py

echo -e "Running autopep8"
autopep8 --in-place --global-config=.flake8 --max-line-length=79 -a -a --exit-code -r ./py_france_rte/* main.py

echo -e "Running pylint"
pylint ./py_france_rte main.py -s=no --max-line-length=79
RETURN_CODE=$?

echo -e "conda env 'rte' : ${RED}deactivate${NOCOLOR}"
conda deactivate

exit $RETURN_CODE