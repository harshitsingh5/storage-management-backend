from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import shutil


gauth = GoogleAuth()
drive = GoogleDrive(gauth)
cur_path = os.path.dirname(__file__)

MIMETYPES = {
        # Drive Document files as MS dox
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Drive Sheets files as MS Excel files.
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        # Drive presentation as MS pptx
        'application/vnd.google-apps.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        # see https://developers.google.com/drive/v3/web/mime-types
        'text/plain': 'text/plain'
    }
EXTENSTIONS = {
        'application/vnd.google-apps.document': '.docx',
        'application/vnd.google-apps.spreadsheet': '.xlsx',
        'application/vnd.google-apps.presentation': '.pptx',
        'text/plain': '.txt',
}

def drive_list_files(folder_id='root'):
    # List files in Google Drive
    x = "\'" + str(folder_id)+"\' in parents and trashed=false"
    fileList = drive.ListFile({'q': x}).GetList()
    data = []
    for file1 in fileList:
        title = file1['title']
        id  = file1['id']
        typee = file1['mimeType'].split('.')[-1]
        mimetype = file1['mimeType']
        # print('title: %s, id: %s' % (file1['title'], file1['id']))
        data.append({'title':title, 'id':id, 'type':typee, 'mimetype':mimetype})
    return data


def drive_upload_file(folder_id):
    file1 = drive.CreateFile({
        'title': 'upload1.txt', 
        # 'parents': [{'id': '1P7Jhy_AJ914eMIG206qCkzHbd-_2OjWI'}]
        })
    mypath = os.path.join(cur_path,'..//files//upload//upload1.txt')
    file1.SetContentFile(mypath)
    file1.Upload()
    # print("Upload Successful")
    return "Upload Successful"


def drive_download_file(file_id, title, mimetype):
    file = drive.CreateFile({'id': file_id})
    download_mimetype = MIMETYPES[mimetype]
    complete_filename = title+EXTENSTIONS[file['mimeType']]
    file.GetContentFile(complete_filename, mimetype=download_mimetype)
    # moving the file
    source = os.path.join(cur_path,'..//') + str(complete_filename)
    dest = os.path.join(cur_path,'..//files//download//') + str(complete_filename)
    shutil.move(source, dest)
    return "Download Successful"


def drive_delete_file(file_id):
    file1 = drive.CreateFile({'id': file_id})
    file1.Trash()
    # file1.UnTrash()
    # file1.Delete()
    return "File Deleted Successfully"


