import os
import boto3
from pathlib import Path
import shutil
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File
from django.utils.module_loading import import_module
from botocore.exceptions import ClientError


def get_cloud_storage():
    module_name, class_name = settings.CLOUD_STORAGE_CLASS.rsplit(".", 1)
    CloudStorageClass = getattr(import_module(module_name), class_name)
    return CloudStorageClass()


class LocalStorage(FileSystemStorage):
    """
    LocalStorage class to handle local file storage.
    """
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.MEDIA_ROOT
        if base_url is None:
            base_url = settings.MEDIA_URL
        super().__init__(location, base_url)

    def _save(self, name, content):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return super()._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name

    def _open(self, name, mode='rb'):
        return File(open(self.path(name), mode))


class LocalCloudStorageBackend:
    """
    LocalCloudStorageBackend class to handle cloud storage operations.
    """

    def create_folder(self, folder_path, content):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, folder_path), exist_ok=True)
        with open(os.path.join(settings.MEDIA_ROOT, folder_path, 'content.txt'), 'w') as f:
            f.write(content)
        import pdb
        pdb.set_trace()
        return os.path.join(settings.MEDIA_ROOT, folder_path, 'content.txt')

    def delete_folder(self, folder_path):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, folder_path), ignore_errors=True)

    def update_folder(self, folder_path, content):
        with open(os.path.join(settings.MEDIA_ROOT, folder_path, 'content.txt'), 'w') as f:
            f.write(content)

    def read_file(self, file_url):
        if not os.path.exists(file_url):
            return ""
        with open(file_url, 'r') as f:
            return f.read()
        
    def file_exist(self, file_url):
        return os.path.exists(file_url)



class Boto3CloudStorageBackend:
    """
    Boto3CloudStorageBackend class to handle cloud storage operations.
    """
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = settings.S3_BUCKET

    def create_folder(self, folder_path, content):
        self.s3_client.put_object(Bucket=self.bucket_name, Key=(folder_path+'/'), Body=content)

    def delete_folder(self, folder_path):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=folder_path)

    def update_folder(self, folder_path, content):
        self.s3_client.put_object(Bucket=self.bucket_name, Key=(folder_path+'/'), Body=content)

    def read_file(self, file_key):
        file = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
        return file['Body'].read().decode('utf-8')
    
    def file_exist(self, file_hey):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_hey)
            return True
        except ClientError:
            return False


