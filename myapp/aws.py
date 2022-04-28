import boto3
import os
from .config import *

cur_path = os.path.dirname(__file__)

def aws_upload_file(bucket_name):
    try:
        s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
        mypath = os.path.join(cur_path,'..//files//upload//upload1.txt')
        s3.meta.client.upload_file(mypath, bucket_name, 'upload1.txt')
        # print("Upload Successful!")
        return "Upload Successful"
    except:
        return "Upload Failed"


def download_file(bucket_name, object_name):
    try:
        s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
        mypath = os.path.join(cur_path,'..//files//download//') + str(object_name)
        s3.meta.client.download_file(bucket_name, object_name, mypath)
        return "Download Successful"
    except:
        return "Download Failed"


def delete_file(bucket_name, object_name):
    try:
        s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
        s3.meta.client.delete_object(Bucket=bucket_name, Key=object_name)
        return "File Deleted Successfully"
    except:
        return "File Deletion Failed"


def list_s3_files(bucket_name):
    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key= aws_secret_access_key)
    fileList = []
    # myBucket = s3.Bucket(aws_bucket)
    myBucket = s3.Bucket(bucket_name)
    for my_bucket_object in myBucket.objects.all():
        fileList.append(my_bucket_object.key)
        # print(my_bucket_object)
    # print(myBucket.objects.all())
    return fileList


def list_all_buckets():
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key= aws_secret_access_key)
    bucketList = []
    all_b = s3.list_buckets()['Buckets']
    # print(all_b)
    for bucket in all_b:
        bucketList.append(bucket['Name'])
        # print(bucket)
    return bucketList


def create_bucket(bucket_name, region=None):
    if region is None:
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key= aws_secret_access_key)
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key= aws_secret_access_key)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
    return "Bucket deleted successfully"


def delete_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key= aws_secret_access_key)
        response = s3_client.delete_bucket(Bucket=bucket_name,)
        # print(response)
        if response.get('ResponseMetadata'):
            return "Bucket deleted successfully"
        else:
            return "Some error occurred"
    except:
        return "Some error occurred"
        
