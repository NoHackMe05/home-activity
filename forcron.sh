#!/bin/bash
#
#

argument=$1

repertoire=$(cd "$(dirname "$0")" && pwd)

if [ ! -d "${repertoire}/mon_env" ]; then
    python3 -m venv ${repertoire}/mon_env
fi

source ${repertoire}/mon_env/bin/activate

cd $repertoire

if [ "$argument" == "info" ]; then
    python3 show_info.py
else
    interfaces=("enp0s3")

    # python3 main.py eth0
    # python3 main.py wlan0
    for interface in "${interfaces[@]}"; do
        python3 main.py "$interface"
    done
fi

deactivate