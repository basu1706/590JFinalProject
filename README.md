# 590JFinalProject
Final Project for CS590J


To test the implant:

1. Download the secrets.json file from Slack into the working directory where all the python scripts are. Save it as exactly "secrets.json".

2. Tar the relevant files:

tar -cvf implant.tar c2_discord.py c2_implant.py helper.py raw_img requirements.txt secret_img start.sh secrets.json finalkey.json

This is the implant

3. Load the implant.tar onto the target and change permissions using
chmod 777 implant.tar

4. Then extract the files using:

tar -xvf implant.tar

(base) basundharachakrabarty@Basundharas-MacBook-Air test % tar -xvf implant.tar
x c2_discord.py
x c2_implant.py
x finalkey.json
x helper.py
x raw_img/
x raw_img/nomemes.png
x raw_img/whatare.png
x requirements.txt
x secret_img/
x secret_img/upload.png
x start.sh
x secrets.json
(base) basundharachakrabarty@Basundharas-MacBook-Air test % ls -l
total 4016
drwxr-xr-x  3 basundharachakrabarty  staff       96 May  2 22:35 __pycache__
-rwxr-xr-x  1 basundharachakrabarty  staff      917 May  2 22:27 c2_discord.py
-rwxr-xr-x  1 basundharachakrabarty  staff     2118 May  2 22:27 c2_implant.py
-rwxr-xr-x  1 basundharachakrabarty  staff     2317 May  2 22:27 finalkey.json
drwxr-xr-x  2 basundharachakrabarty  staff       64 May  2 22:35 gitFiles
-rw-r--r--  1 basundharachakrabarty  staff  2021376 May  2 22:39 implant.tar
-rwxr-xr-x  1 basundharachakrabarty  staff     7545 May  2 22:27 helper.py
drwxrwxrwx  4 basundharachakrabarty  staff      128 May  2 22:39 raw_img
-rwxr-xr-x  1 basundharachakrabarty  staff      185 May  2 22:27 requirements.txt
drwxrwxrwx  3 basundharachakrabarty  staff       96 May  2 22:39 secret_img
-rw-r--r--@ 1 basundharachakrabarty  staff      346 May  2 22:36 secrets.json
-rwxr-xr-x  1 basundharachakrabarty  staff      114 May  2 22:27 start.sh

5. Run the bash script sh ./start.sh which runs the python scripts individually
