import os
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from logger_config import setup_logger

logger = setup_logger()

# ----- إنشاء service_account.json من الـ Environment Variable -----
if os.environ.get("SERVICE_ACCOUNT_JSON"):
    creds_json = os.environ["SERVICE_ACCOUNT_JSON"]

    # إزالة أي أسطر جديدة زائدة
    creds_json = creds_json.replace("\\n", "\n")

    # كتابة الملف
    with open("service_account.json", "w", encoding="utf-8") as f:
        f.write(creds_json)

SERVICE_ACCOUNT_JSON_PATH = "service_account.json"


class GoogleDriveUploader:
    def __init__(self, creds_file= SERVICE_ACCOUNT_JSON_PATH):
        
        try:
            self.creds = service_account.Credentials.from_service_account_file(
                creds_file,
                scopes=["https://www.googleapis.com/auth/drive"]
            )

            self.service = build("drive", "v3", credentials=self.creds)
            logger.info("Google Drive service initialized")

        except Exception as e:
            logger.error(f"Error initializing Google Drive: {str(e)}")
            raise e

    def upload_file(self, file_path, folder_id):
        try:
            file_name = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)

            file_metadata = {
                "name": file_name,
                "parents": [folder_id]
            }

            media = MediaFileUpload(file_path, mimetype=mime_type)

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            file_id = file.get("id")
            logger.info(f"File uploaded: {file_name} | ID: {file_id}")
            return file_id

        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {str(e)}")
            return None

    def get_folder_id_by_name(self, parent_id, folder_name):
        try:
            query = f"'{parent_id}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()

            folders = results.get("files", [])
            if not folders:
                logger.warning(f"Folder not found: {folder_name}")
                return None

            folder_id = folders[0]["id"]
            logger.info(f"Folder found: {folder_name} | ID: {folder_id}")
            return folder_id

        except Exception as e:
            logger.error(f"Error finding folder {folder_name}: {str(e)}")
            return None

    def get_month_folder(self, year_folder_id, month_number):
        try:
            month_map = {
                1: "1 Jan", 2: "2 Feb", 3: "3 Mar", 4: "4 Apr",
                5: "5 May", 6: "6 Jun", 7: "7 Jul", 8: "8 Aug",
                9: "9 Sep", 10: "10 Oct", 11: "11 Nov", 12: "12 Dec"
            }
            folder_name = month_map.get(month_number)
            if not folder_name:
                logger.error(f"Invalid month number: {month_number}")
                return None

            return self.get_folder_id_by_name(year_folder_id, folder_name)
        except Exception as e:
            logger.error(f"Error getting month folder: {str(e)}")
            return None
