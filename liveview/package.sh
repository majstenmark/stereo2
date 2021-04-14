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

out=SP-Liveview

rm_if_exist $out
rm_if_exist $out.zip
mkdir $out
ximea="bin/XIMEA_Linux_SP.tgz"
jfx="bin/openjfx-11.0.2_linux-x64_bin-sdk.zip"
exists_check $ximea
exists_check $jfx
mkdir $out/bin
cp $ximea $out/bin
cp $jfx $out/bin

cp -r src $out
rm_if_exist python/__pycache__
cp -r python $out
cp Makefile $out
cp install.sh $out
cp -r LUT $out

zip -r $out.zip $out 
rm_if_exist $out

