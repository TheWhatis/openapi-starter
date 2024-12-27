#!/usr/bin/sh
#==
#   NOTE      - split
#   Author    - Whatis
#
#   Created   - 2024.12.26
#   Github    - ...
#   Contact   - asdwdagwahwabe@gmail.com
#/

root=$(dirname $0);
splDir="$root/split";
script="$splDir/main.py";
requirements="$splDir/requirements.txt";
activate="$splDir/bin/activate";


if [ ! -f $activate ]; then
    echo Generate venv and install requirements

    python -m venv $splDir
    source $activate
    pip install -r $requirements
fi

source $activate

python $script $@

deactivate
