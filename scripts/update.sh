#! /bin/bash

source .linvenv/bin/activate

python3 -m pip install -r etc/requirements.txt

deactivate

echo 'done'
