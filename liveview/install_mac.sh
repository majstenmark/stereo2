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
brew=`which brew`
if [ -z "$brew" ] ; then
    echo "Installing homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
else
    echo "Brew is installed"
fi

function install_p3 {
    echo "installing python3 + opencv"
    brew install python3
    python3 -m pip install opencv-python 
    python3 -m pip install numpy progress
}


function install_jfx {
    echo "installing java11 and javafx"
    #sudo apt install openjdk-11-jdk
    brew tap AdoptOpenJDK/openjdk
    brew install adoptopenjdk11 --no-quarantine
    
    mkdir -p bin
    cp libs/openjfx-11.0.2_osx-x64_bin-sdk.zip bin/

    cd bin
    rm_if_exist javafx-sdk-11.0.2
    unzip openjfx-11.0.2_osx-x64_bin-sdk.zip > jfx_install.log
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

function check_ximea {
    echo "Checking Ximea installation"

    text="try:\n\timport ximea\n\tprint(ximea.__version__)\nexcept: print('Missing')"
    OUT=`echo -e "$text" | python`
    if [ "$OUT" = "Missing" ]; then
        echo "Manually install Ximea from https://www.ximea.com/support/wiki/apis/XIMEA_macOS_Software_Package"
    else
        echo "Installation finished!"
    fi
}

install_p3
install_jfx
dl_demo
check_ximea