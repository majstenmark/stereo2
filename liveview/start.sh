#!/bin/bash

#!/bin/bash
cd "${0%/*}"
d=$(date "+%Y%m%d-%H%M%S")
folder=~/.liveview_log
mkdir -p $folder
make usb > >(tee -a $folder/$d-stdout.log) 2> >(tee -a $folder/$d-stderr.log >&2)
