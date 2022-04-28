from django.urls import include, path
from django.views.generic.base import TemplateView

from django.urls import re_path
from .views import *

urlpatterns = [
    path('aws/buckets/', AwsBuckets.as_view()),
    path('aws/files-all/', AwsListFiles.as_view()),
    path('aws/files/', AwsFiles.as_view()),

    path('drive/files-all/', DriveListFiles.as_view()),
    path('drive/files/', DriveFiles.as_view()),

    path('dropbox/folders/', DropboxFolders.as_view()),
    path('dropbox/files-all/', DropboxListFiles.as_view()),
    path('dropbox/files/', DropboxFiles.as_view()),
]