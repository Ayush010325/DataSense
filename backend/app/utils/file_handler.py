import os
import shutil
from fastapi import UploadFile

# Store files in a directory named 'data_storage' parallel to 'app'
STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")

def save_upload_file(upload_file: UploadFile, dest_filename: str) -> str:
    """
    Saves an uploaded file to the local data_storage directory.
    Returns the absolute path to the saved file.
    """
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
        
    file_path = os.path.join(STORAGE_DIR, dest_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_path
