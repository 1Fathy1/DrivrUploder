# File Uploader Bot
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)

A Telegram bot to upload files to Google Drive, organized by year and month folders.  
Supports PDF, Word, and files with Arabic characters.  

---

## Features

- Upload files automatically to Google Drive  
- Choose the target month (January → December)  
- Supports Arabic filenames  
- Logs all uploads in `logger.log`  
- Compatible with Render for 24/7 operation  
- Sensitive data protected using `.env` or Render Secrets  

---

## Requirements

- Python 3.10+  
- Google Service Account  
- Shared Drive folder with Editor permissions  
- Telegram Bot Token from BotFather  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/file-uploader-bot.git
cd file-uploader-bot