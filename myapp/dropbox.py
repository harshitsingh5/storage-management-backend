from .config import *
import dropbox
import os
import pathlib

cur_path = os.path.dirname(__file__)

def dropbox_list_files(folder_path=""):
    try:
        dbx = dropbox.Dropbox(dropbox_access_token)
        data = []
        response = dbx.files_list_folder(folder_path)
        for file in response.entries:
            # print(file)
            # print('--------------------------------')
            data.append({'name':file.name, 'id':file.id, 'type': str(type(file)), 'path_display': file.path_display})
        return data
    except Exception as e:
        return('Error getting list of files from Dropbox: ' + str(e))


def dropbox_upload_file(local_path, local_file, dropbox_file_path=""):
    try:
        dbx = dropbox.Dropbox(dropbox_access_token)
        local_file_path = pathlib.Path(os.path.join(cur_path,'..//files//upload//upload1.txt'))
        dropbox_file_path += '/upload1.txt'
        # with local_file_path.open("rb") as f:
        with open(local_file_path, 'rb') as f:
            meta = dbx.files_upload(f.read(), path=dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"), mute=True)
            # print(meta.path_display)
            return "Upload Successful"
    except Exception as e:
        return('Error uploading file to Dropbox: ' + str(e))


def dropbox_download_file(filename, dropbox_file_path):
    try:
        dbx = dropbox.Dropbox(dropbox_access_token)
        mypath = os.path.join(cur_path,'..//files//download//') + str(filename)
        with open(mypath, 'wb') as f:
            metadata, result = dbx.files_download(path=dropbox_file_path)
            f.write(result.content)
        return 'File downloaded successfully'
    except Exception as e:
        return('Error downloading file from Dropbox: ' + str(e))


def dropbox_delete_file(dropbox_path):
    dbx = dropbox.Dropbox(dropbox_access_token)
    file1 = dbx.files_delete_v2(dropbox_path)
    # print(file1)
    return "Deleted Successfully"


def dropbox_create_folder(folder_name, dropbox_path):
    dbx = dropbox.Dropbox(dropbox_access_token)
    final_p = dropbox_path + '/' + folder_name
    a = dbx.files_create_folder(final_p)
    return "Folder created successfully"

#