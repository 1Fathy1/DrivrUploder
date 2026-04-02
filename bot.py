from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from drive_uploader import GoogleDriveUploader
from logger_config import setup_logger, log_upload
import os
from dotenv import load_dotenv
load_dotenv()

# ---------------- CONFIG ----------------

BOT_TOKEN = os.getenv("BOT_TOKEN")
YEAR_FOLDER_ID = os.getenv("YEAR_FOLDER_ID")
ALLOWED_USERS = ["fa_th_y"]  # Add allowed Telegram usernames

# ----- إنشاء service_account.json من الـ Environment Variable -----
if os.environ.get("SERVICE_ACCOUNT_JSON"):
    creds_json = os.environ["SERVICE_ACCOUNT_JSON"]

    # إزالة أي أسطر جديدة زائدة
    creds_json = creds_json.replace("\\n", "\n")

    # كتابة الملف
    with open("service_account.json", "w", encoding="utf-8") as f:
        f.write(creds_json)

SERVICE_ACCOUNT_JSON_PATH = "service_account.json"
uploader = GoogleDriveUploader()
logger = setup_logger()

# ---------------- USERS STATE ----------------
user_files = {}  # {chat_id: {"file_path": str, "username": str}}

# ---------------- MONTH BUTTONS ----------------
month_buttons = [
    [InlineKeyboardButton("1 Jan", callback_data="1")],
    [InlineKeyboardButton("2 Feb", callback_data="2")],
    [InlineKeyboardButton("3 Mar", callback_data="3")],
    [InlineKeyboardButton("4 Apr", callback_data="4")],
    [InlineKeyboardButton("5 May", callback_data="5")],
    [InlineKeyboardButton("6 Jun", callback_data="6")],
    [InlineKeyboardButton("7 Jul", callback_data="7")],
    [InlineKeyboardButton("8 Aug", callback_data="8")],
    [InlineKeyboardButton("9 Sep", callback_data="9")],
    [InlineKeyboardButton("10 Oct", callback_data="10")],
    [InlineKeyboardButton("11 Nov", callback_data="11")],
    [InlineKeyboardButton("12 Dec", callback_data="12")]
]
month_markup = InlineKeyboardMarkup(month_buttons)

# ---------------- COMMANDS ----------------
async def start(update: Update, context: CallbackContext):
    username = update.message.from_user.username or update.message.from_user.full_name
    if username not in ALLOWED_USERS:
        await update.message.reply_text("❌ You are not allowed to use this bot.")
        return

    await update.message.reply_text(
        "👋 Hi! Welcome to the File Uploader Bot.\n\n"
        "You can:\n"
        "1️⃣ Send a file to upload.\n"
        "2️⃣ Choose the month folder it should be uploaded to.\n\n"
        "Please send your file to begin."
    )

# ---------------- FILE HANDLER ----------------
async def handle_file(update: Update, context: CallbackContext):
    username = update.message.from_user.username or update.message.from_user.full_name
    chat_id = update.message.chat_id

    if username not in ALLOWED_USERS:
        await update.message.reply_text("❌ You are not allowed to upload files.")
        return

    file = update.message.document
    if not file:
        await update.message.reply_text("Please send a document.")
        return

    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{file.file_name}"
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)

    user_files[chat_id] = {"file_path": file_path, "username": username}
    await update.message.reply_text("✅ File received! Now choose the month to upload it to:", reply_markup=month_markup)

# ---------------- CALLBACK QUERY ----------------
async def handle_month_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    month_number = int(query.data)
    chat_id = query.message.chat_id
    username = query.from_user.username or query.from_user.full_name

    if username not in ALLOWED_USERS:
        await query.message.reply_text("❌ You are not allowed to use this bot.")
        return

    if chat_id not in user_files:
        await query.message.reply_text("No file found. Send a file first.")
        return

    user_data = user_files.pop(chat_id)
    file_path = user_data["file_path"]

    folder_id = uploader.get_month_folder(YEAR_FOLDER_ID, month_number)
    if not folder_id:
        await query.message.reply_text("Folder not found on Drive. Contact admin.")
        return

    file_id = uploader.upload_file(file_path, folder_id)

    if file_id:
        await query.message.reply_text(f"✅ File uploaded successfully to month {month_number}!")
        log_upload(username, os.path.basename(file_path), f"{month_number}")
        os.remove(file_path)  # clean up local file
    else:
        await query.message.reply_text("❌ Upload failed. Try again later.")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(CallbackQueryHandler(handle_month_choice))

    print("Bot is running...")
    app.run_polling()
