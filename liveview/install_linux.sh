#!/bin/bash

function rm_if_exist {
    [ ! -e $1 ] || rm -r $1
}

function exists_check {
    if [ ! -e $1 ] ; then
        echo "Can't find $1, aborting.."
        exit 1
    fi
}

function install_p3 {
    echo "installing python3 + opencv"
    sudo apt install python3-pip python3-opencv libopencv-dev
    python3 -m pip install numpy progress --user
}

function install_ximea {
    mkdir -p bin
    cd bin
    echo "installing ximea"
    if [ ! -e XIMEA_Linux_SP.tgz ]; then
        wget https://www.ximea.com/downloads/recent/XIMEA_Linux_SP.tgz
    fi
    rm_if_exist ximea
    rm_if_exist package
    exists_check XIMEA_Linux_SP.tgz
    tar xzf XIMEA_Linux_SP.tgz
    mv package ximea
    cd ximea && ./install > install_log.log && cd ..
    cd ..
}

function install_jfx {
    echo "installing java11 and javafx"
    sudo apt install openjdk-11-jdk
    mkdir -p bin
    cp libs/openjfx-11.0.2_linux-x64_bin-sdk.zip bin/

    cd bin
    rm_if_exist javafx-sdk-11.0.2
    unzip openjfx-11.0.2_linux-x64_bin-sdk.zip > jfx_install.log
    cd ..
}

function dl_demo {
    if [ ! -e "mock-stream" ] ; then 
        mkdir mock-stream
        cd mock-stream
        echo "Downloading demo video files"
        wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1E9Mqml08VLph07NMR1e_V3v68dpu6cyg' -O cam_R.mp4
        wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15MdcmijWSwt2xvH60TfpLN-8Fkl70NIs' -O cam_L.mp4
        cd ..
    fi
}

install_p3
install_ximea
install_jfx
dl_demo
python3 create_desktop_img.py

echo "Installation finished"