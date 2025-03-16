#!/bin/bash

function VSC_Build {
    # Description: Build script for VSC
    python VSC.py init
    python VSC.py add ./myfile.txt
    python VSC.py commit -m "Initial commit"
    python VSC.py log
    python VSC.py branch feature-x
    python VSC.py switch feature-x
    rm -rf ./.Byte/
    clear
}

function PyBuild {
    pip install pyinstaller
    pyinstaller --onefile --icon=favicon.ico ./VSC.py
}

read -p "Enter the command to run: " command
if [ "$command" == "VSC" ]; then
    VSC_Build
elif [ "$command" == "PyBuild" ]; then
    PyBuild
else
    echo "Invalid command"
fi
