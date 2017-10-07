#!/bin/bash

# if cannot run, do command
#    chmod +x install_pkg.sh

pip3 install requests
pip3 install numpy
pip3 install sumy

python3 "./nltk_download.py"
