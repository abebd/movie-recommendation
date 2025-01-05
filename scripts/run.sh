#! /bin/bash

source .linvenv/bin/activate

#python3 -m pip install -r etc/requirements.txt

python3 ../movie-recommendation #--list_new

deactivate
