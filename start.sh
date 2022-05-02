#!/bin/bash
pip install -r requirements.txt &&
python c2_impant.py &
python packetsniff.py &
