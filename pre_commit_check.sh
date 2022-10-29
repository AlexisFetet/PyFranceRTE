#!/bin/bash

conda.bat activate rte

echo "running isort" 
isort ./*
echo "running autopep8" 
autopep8 --in-place --global-config=.flake8 --max-line-length=79 -a -a -r ./py_france_rte/* main.py
echo "running pylint" 
pylint ./py_france_rte main.py --disable=too-many-arguments --disable=too-few-public-methods -s=no