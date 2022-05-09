# from sys import api_version
# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .aws import *
from .drive import *
from .dropbox import *
import os

cur_path = os.path.dirname(__file__)
MIMETYPES = {
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
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


class AwsFiles(GenericAPIView):
    queryset = []

    def get(self, request):
        bucket_name = request.GET['bucket_name']
        object_name = request.GET['object_name']
        res = download_file(bucket_name, object_name)
        data = {'file':object_name, 'status':res}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        bucket_name = request.data['bucket_name']
        res = aws_upload_file(bucket_name)
        data = {'file': 'filename', 'status':res}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        bucket_name = request.data['bucket_name']
        object_name = request.data['object_name']
        res = delete_file(bucket_name, object_name)
        data = {'file': object_name, 'status':res}
        return Response(data, status=status.HTTP_200_OK)


class AwsListFiles(GenericAPIView):
    queryset = []
    def post(self, request):
        bucket_name = request.data['bucket_name']
        fileList = list_s3_files(bucket_name)
        queryset = fileList
        data = {'fileList': fileList}
        return Response(data=data, status=status.HTTP_200_OK)


class AwsBuckets(GenericAPIView):
    queryset = []
    def get(self, request):
        bucketList = list_all_buckets()
        queryset = bucketList
        data = {'bucketList': bucketList}
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        bucket_name = request.data['bucket_name']
        if create_bucket(bucket_name=bucket_name, region='ap-south-1'):
            data = {'bucketName': bucket_name, 'status': 'Bucket created'}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {'bucketName': 'NA', 'status': 'Bucket NOT created'}
            return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request):
        bucket_name = request.data['bucket_name']
        res = delete_bucket(bucket_name)
        if res == 'Bucket deleted successfully':
            data = {'bucket_name':bucket_name, 'status':res}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {'bucket_name':bucket_name, 'status':res}
            return Response(data=data, status=status.HTTP_200_OK)



class DriveListFiles(GenericAPIView):
    queryset = []
    def post(self, request):
        folder_id = request.data['folder_id']
        fileList = drive_list_files(folder_id)
        queryset = fileList
        data = {'fileList': fileList}
        return Response(data=data, status=status.HTTP_200_OK)


class DriveFiles(GenericAPIView):
    queryset = []

    def get(self, request):
        file_id = request.GET['file_id']
        title = request.GET['title']
        mimetype = request.GET['mimetype']
        res = drive_download_file(file_id, title,mimetype)
        complete_filename = title+EXTENSTIONS[mimetype]
        mypath = os.path.join(cur_path,'..//files//download//') + str(complete_filename)
        with open(mypath, 'rb') as f:
            res = FileWrapper(f)
            return HttpResponse(res, status=status.HTTP_200_OK)
        data = {'file':title, 'status':res}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        folder_id = request.data['folder_id']
        res = drive_upload_file(folder_id)
        data = {'file': 'filename', 'status':res}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        file_id = request.data['file_id']
        res = drive_delete_file(file_id)
        data = {'file': file_id, 'status':res}
        return Response(data, status=status.HTTP_200_OK)


class DropboxListFiles(GenericAPIView):
    queryset = []
    def post(self, request):
        folder_path = request.data['folder_path']
        fileList = dropbox_list_files(folder_path)
        queryset = fileList
        data = {'fileList': fileList, 'currentPath': folder_path}
        return Response(data=data, status=status.HTTP_200_OK)


class DropboxFiles(GenericAPIView):
    queryset = []

    def get(self, request):
        filename = request.GET['filename']
        filepath = request.GET['filepath']
        res = dropbox_download_file(filename, filepath)
        mypath = os.path.join(cur_path,'..//files//download//') + str(filename)
        with open(mypath, 'rb') as f:
            res = FileWrapper(f)
            return HttpResponse(res, status=status.HTTP_200_OK)
        # data = {'file':filename, 'data':res}
        data = {'result':res}
        return HttpResponse(res, status=status.HTTP_200_OK)

    def post(self, request):
        dropbox_file_path = request.data['dropbox_file_path']
        local_path = ''
        local_file = ''
        res = dropbox_upload_file(local_path, local_file, dropbox_file_path)
        data = {'file': 'filename', 'status':res}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        dropbox_path = request.data['dropbox_path']
        res = dropbox_delete_file(dropbox_path)
        data = {'file': dropbox_path, 'status':res}
        return Response(data, status=status.HTTP_200_OK)


class DropboxFolders(GenericAPIView):
    queryset = []
    # def get(self, request):
    #     bucketList = list_all_buckets()
    #     queryset = bucketList
    #     data = {'bucketList': bucketList}
    #     return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        folder_name = request.data['folder_name']
        dropbox_path = request.data['dropbox_path']
        res = dropbox_create_folder(folder_name, dropbox_path)
        data = {'folder_name':folder_name, 'status':res}
        return Response(data, status=status.HTTP_200_OK)
        

    def delete(self, request):
        bucket_name = request.data['bucket_name']
        res = delete_bucket(bucket_name)
        if res == 'Bucket deleted successfully':
            data = {'bucket_name':bucket_name, 'status':res}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {'bucket_name':bucket_name, 'status':res}
            return Response(data=data, status=status.HTTP_200_OK)

#