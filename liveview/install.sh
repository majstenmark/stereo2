#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    echo "Installing on Linux"
    ./install_linux.sh
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    #Mac OS
    echo "Installing on mac"
    ./install_mac.sh
else
    echo "Unknown OS, see README.md for manuall installation"
fi

