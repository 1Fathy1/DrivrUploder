from drive_uploader import GoogleDriveUploader

YEAR_FOLDER_ID = "10z8oPv7LoowNdwSGiuOHwQcmpi8qmqbN"

def main():
    try:
        uploader = GoogleDriveUploader()
        file_path = "test.pdf"

        # simulate user choice
        selected_month = 12  # March

        folder_id = uploader.get_month_folder(YEAR_FOLDER_ID, selected_month)

        if not folder_id:
            print("Folder not found")
            return

        file_id = uploader.upload_file(file_path, folder_id)

        if file_id:
            print("Upload Success (Private)")
        else:
            print("Upload Failed")

    except Exception as e:
        print("Fatal Error:", str(e))

if __name__ == "__main__":
    main()