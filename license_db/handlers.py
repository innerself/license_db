import os
from shutil import rmtree

from typing import Optional, Union

from django.conf import settings
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile
)


def save_to_disk(
        file: Union[TemporaryUploadedFile, InMemoryUploadedFile],
        folder: Optional[str]='uploads',
    ) -> dict:

    folder_path = os.path.join(settings.BASE_DIR, folder)
    file_path = os.path.join(folder_path, file.name)

    if os.path.exists(folder_path):
        rmtree(folder_path)

    os.mkdir(folder_path)

    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    file_info = {
        'name': file.name,
        'path': file_path,
    }

    return file_info
