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

out=debayer_app

rm_if_exist $out
rm_if_exist $out.zip
mkdir $out
cp -r *.js $out
cp -r *.html $out
cp -r css $out
rm_if_exist python/__pycache__
cp -r python $out
cp README.md $out
cp package.json $out
cp package-lock.json $out
cp *.sh $out
cp icon256.png $out
cp *.py $out
cp raw_table.data $out

zip -r $out.zip $out 
rm_if_exist $out
