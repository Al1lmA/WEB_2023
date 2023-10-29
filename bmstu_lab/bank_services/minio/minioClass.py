from minio import Minio
from minio.error import S3Error
from io import BytesIO
from base64 import b64encode, b64decode
import os
import pip._vendor.requests as requests
import io
from datetime import timedelta


from minio import Minio

# опциональный параметр, отвечающий за вкл/выкл защищенное TLS соединение

class MinioClass:
    def __init__(self):
        try:
            self.client = Minio(endpoint="192.168.100.187:9000",
                                access_key='minioadmin',
                                secret_key='minioadmin',
                                secure=False)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def addUser(self, username: str):
        try:
            self.client.make_bucket(username)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def removeUser(self, username: str):
        try:
            self.client.remove_bucket(username)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def addImage(self, bucket: str, title: str, image_url: str):
        try:
            response = requests.get(image_url)
            image_stream = io.BytesIO(response.content)
            self.client.put_object(bucket_name=bucket,
                                   object_name=f"{title}.png",
                                   data=image_stream,
                                   length=len(response.content))
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def getImage(self, bucket: str, title: str):
        try:
            result = self.client.get_presigned_url(
                method='GET',
                bucket_name=bucket,
                object_name=f"{title}.png",
                expires=timedelta(minutes=1),
                )
            # print (result)
            return result
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def removeImage(self, bucket: str, title: str):
        try:
            self.client.remove_object(bucket_name=bucket,
                                      object_name=f"{title}.png")
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def check_bucket_exists(self, bucket_name):
        info_bucket = self.client.bucket_exists(bucket_name)
        if (info_bucket):
            print(f'[{info_bucket}] Бакет "{bucket_name}" существует')
        else:
            print(f'[{info_bucket}] Бакет "{bucket_name}" не существует')