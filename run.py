from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
from datetime import date
import uuid

scopes = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('finalkey.json', scopes)
driveService = build('drive', 'v3', credentials=creds)
parentDir='1cfjlBcYJPEdcHBoc3aa94zPvnUfJTCSm'
UUID=hex(uuid.getnode())
mime_types={'folder':'application/vnd.google-apps.folder','text':'text/plain'}


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

today=date.today()
date_folder_name=today.strftime("%d_%m_%Y")


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
        uploadFile('test.tar.gz','application/tar',date_folder_id)
    else:
        print("Uploading file to date folder!")
        uploadFile('test.tar.gz','application/tar',date_folder_id)




"""
'application/tar'
files=['test.txt']

for file,mime_type in zip(files,mime_types):
    print ("Uploading file " + file + "...")
    metadata = {
        'name': file, 
        "parents": [folder_id]
        }

    #Now create the media file upload object and tell it what file to upload,
    #in this case 'test.html'
    media = MediaFileUpload('test.txt', mimetype = 'text/plain')

    #Now we're doing the actual post, creating a new file of the uploaded type
    file = driveService.files().create(body=metadata, media_body=media,fields='id').execute()

    #Because verbosity is nice
    print("Created file '%s' id '%s'." % (file.get('name'), file.get('id')))

"""