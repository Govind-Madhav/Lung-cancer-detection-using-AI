import shutil
import os

def save_upload_file_tmp(upload_file, destination):
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
