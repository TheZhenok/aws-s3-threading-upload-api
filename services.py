# Typing
from typing import Union, Optional

# Python
import threading
import boto3
import botocore
from tempfile import SpooledTemporaryFile
import uuid

# Local
import config
from config import logger


class FileHandler:
    """
    Объект Singleton для создания единого подключения
    """

    def __init__(self) -> None:
        self.S3_CLIENT = boto3.client('s3',
                            aws_access_key_id=config.S3_ACCESS_KEY,
                            aws_secret_access_key=config.S3_SECRET_KEY)
        self.threads: list[threading.Thread] = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileHandler, cls).__new__(cls)
        return cls.instance

    def upload_part(
            self,
            key: str, 
            upload_id: str, 
            part_number: int, 
            data: any, 
            result: list[dict],
            attempts=0
            ) -> Optional[dict]:
        """
        Загрузка одной части файла на S3.
        """

        try:
            res = self.S3_CLIENT.upload_part(Bucket=config.S3_BUCKET_NAME, 
                                             Key=key, 
                                             UploadId=upload_id,
                                             PartNumber=part_number, 
                                             Body=data)
            result.append(
                {'ETag': res['ETag'], 'PartNumber': part_number}
            )
        except botocore.exceptions.ClientError as e:
            logger.error(e)
            
            # 6 попыток на повторную загрузку части
            if attempts >= config.MAX_ATTEMPTS_UPLOAD_TO_S3:
                return
            
            logger.info("Trying again")
            self.upload_part(key, upload_id,
                             part_number, data, result)
            attempts += 1

    def upload_to_s3(self, file: SpooledTemporaryFile) -> None:
        """
        Загрузка файла на S3 с помощью многопоточности.
        """

        # Создание мультипарного загрузчика на S3.
        filename: str = f'{uuid.uuid4()}.{file.filename.split(".")[-1]}'
        response: dict[str, Union[dict, str]] = self.S3_CLIENT.create_multipart_upload(
            Bucket=config.S3_BUCKET_NAME, 
            Key=filename
        )
        upload_id = response['UploadId']

        # Определение размера части файла, которую будем загружать.
        part_size = config.COUNT_MB_PER_PART_OF_THE_FILE * 1024 * 1024  # COUNT_MB_PER_PART_OF_THE_FILE (default 30)MB

        # Чтение файла и разбиение на части.
        parts: list[dict] = []
        part_number: int = 1

        # Создание потоков и загрузка частей на S3.
        while True:
            if len(self.threads) == config.COUNT_THREADS:
                for thread in self.threads:
                    thread.join()
                self.threads.clear()

            part = file.read(part_size) # Загружаем части по COUNT_MB_PER_PART_OF_THE_FILE (default 30) МБ
            if not part:
                break
            
            thread = threading.Thread(
                target=self.upload_part, 
                args=(filename, upload_id, part_number, part, parts)
            )
            self.threads.append(thread)
            thread.start()
            print(part_number)
            part_number += 1
            logger.info(f'PART: {part_number}')

        # Ожидание завершения остальных потоков.
        for thread in self.threads:
            thread.join()
        parts = sorted(parts, key=lambda item: item['PartNumber']) 

        # Завершение мультипарной загрузки и объединение частей.
        self.S3_CLIENT.complete_multipart_upload(
            Bucket=config.S3_BUCKET_NAME, 
            Key=filename, 
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        logger.info(f'File {file.name} uploaded to S3 bucket {config.S3_BUCKET_NAME} with key {filename}')
