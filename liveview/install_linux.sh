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

echo "python3 + opencv"
sudo apt-get install python3-pip python3-opencv libopencv-dev
python3 -m pip install numpy progress --user

echo "npm installation"
sudo apt-get update
sudo apt install nodejs-dev node-gyp libssl1.0-dev
cd cut 
sudo apt install npm
npm install
cd ..
cd postprocessing 
sudo apt install npm
npm install
cd ..
cd debayer 
sudo apt install npm
npm install
cd ..


mkdir bin
cd bin
echo "Ximea"
rm_if_exist ximea
rm_if_exist package
if [ ! -e XIMEA_Linux_SP.tgz ]; then
    wget https://www.ximea.com/downloads/recent/XIMEA_Linux_SP.tgz    
fi
exists_check XIMEA_Linux_SP.tgz
tar xzf XIMEA_Linux_SP.tgz
mv package ximea
cd ximea && ./install > install_log.log && cd ..

echo "javafx"
rm_if_exist javafx-sdk-11.0.2
if [ ! -e openjfx-11.0.2_linux-x64_bin-sdk.zip ]; then
    echo "Download openjfx from https://gluonhq.com/products/javafx/ manually and save it in /bin and rerun install.sh"
    exit 1
fi
unzip openjfx-11.0.2_linux-x64_bin-sdk.zip > jfx_install.log

sudo apt install openjdk-11-jdk

cd ..

mkdir mock-stream
cd mock-stream
echo "Downloading demo video files"
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1E9Mqml08VLph07NMR1e_V3v68dpu6cyg' -O cam_R.mp4
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15MdcmijWSwt2xvH60TfpLN-8Fkl70NIs' -O cam_L.mp4

cd ..


python3 create_desktop_img.py
echo "Installation finished"

