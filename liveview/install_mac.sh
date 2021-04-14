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
if [ -z "$brew" ]
then
    echo "Installing homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

else
    echo "Brew is installed"
fi

echo "python3 + opencv"
brew install python3
python3 -m pip install opencv-python 
python3 -m pip install numpy progress
cd cut 
brew install node
cd ..
cd postprocessing
brew install node
cd ..
cd debayer 
brew install node
cd ..

mkdir bin
cd bin


echo "javafx"
rm_if_exist javafx-sdk-11.0.2
if [ ! -e openjfx-11.0.2_osx-x64_bin-sdk.zip ]; then
    echo "Download openjfx from https://gluonhq.com/products/javafx/ manually and rerun install.sh"
    exit 1
fi
unzip openjfx-11.0.2_osx-x64_bin-sdk.zip > jfx_install.log


brew tap AdoptOpenJDK/openjdk
brew cask install adoptopenjdk11 --no-quarantine

echo "Checking Ximea installation"

text="try:\n\timport ximea\n\tprint(ximea.__version__)\nexcept: print('Missing')"
OUT=`echo -e "$text" | python`
if [ "$OUT" = "Missing" ]; then
    echo "Manually install Ximea from https://www.ximea.com/support/documents/4"
fi


cd ..

mkdir mock-stream
cd mock-stream
echo "Downloading demo video files"

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1E9Mqml08VLph07NMR1e_V3v68dpu6cyg' -O cam_R.mp4
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15MdcmijWSwt2xvH60TfpLN-8Fkl70NIs' -O cam_L.mp4
cd ..

echo "Installation finished"

