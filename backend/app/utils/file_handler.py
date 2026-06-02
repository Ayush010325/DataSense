import os
import shutil
from fastapi import UploadFile


STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")


def save_upload_file(upload_file: UploadFile, dest_filename: str) -> str:
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    file_path = os.path.join(STORAGE_DIR, dest_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path
