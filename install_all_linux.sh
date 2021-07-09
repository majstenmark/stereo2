#!/bin/bash

cd liveview ; ./install_linux.sh ; cd ..

cd postprocessing
cd debayer ; ./install.sh ; cd ..
cd merge_tb ;   ./install.sh ; cd ..
cd ..
