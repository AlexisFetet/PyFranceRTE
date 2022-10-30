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
    echo -e "${BLUE}conda env 'rte' : ${GREEN}exists${NOCOLOR}"
else
    echo -e "${BLUE}conda env 'rte' : ${RED}does not exists${NOCOLOR}"
    echo -e "${BLUE}conda env 'rte' : ${GREEN}creating${NOCOLOR}"
    conda env create -n rte -f environment.yml
    echo -e "${BLUE}conda env 'rte' : ${GREEN}created${NOCOLOR}"
fi

echo -e "${Purple}conda env 'rte' : ${GREEN}activate${NOCOLOR}"
conda activate rte
echo -e "${BLUE}Running pycln${NOCOLOR}"
python -m pycln ./* main.py -a -s
echo -e "${BLUE}Running isort${NOCOLOR}" 
python -m isort ./* main.py
echo -e "${BLUE}Running autopep8${NOCOLOR}" 
python -m autopep8 --in-place --global-config=.flake8 --max-line-length=79 -a -a -r ./py_france_rte/* main.py
echo -e "${BLUE}Running pylint${NOCOLOR}" 
python -m pylint ./py_france_rte main.py -s=no
RETURN_CODE=$?
echo -e "${Purple}conda env 'rte' : ${RED}deactivate${NOCOLOR}"
conda deactivate
exit $RETURN_CODE