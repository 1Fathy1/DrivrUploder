import logging
import sys
import os

def setup_logger(log_file="logger.log"):
    logger = logging.getLogger("FileUploaderBot")
    logger.setLevel(logging.INFO)

    # ===== StreamHandler للكونسول =====
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)

    # ===== FileHandler للملف =====
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # منع تكرار handlers
    if not logger.handlers:
        logger.addHandler(sh)
        logger.addHandler(fh)

    return logger

# دالة تسجيل رفع الملفات
def log_upload(user, file_name, folder_name):
    logger = logging.getLogger("FileUploaderBot")
    logger.info("User: %s | File: %s | Folder: %s", user, file_name, folder_name)