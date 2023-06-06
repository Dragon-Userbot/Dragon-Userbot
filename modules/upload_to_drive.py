import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import format_exc
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set up your Google Drive API credentials
API_KEY = "YOUR_API_KEY"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
TOKEN_FILE = "token.json"

# Set up your Google Drive folder ID
FOLDER_ID = "YOUR_FOLDER_ID"


async def upload_file_to_drive(file_path: str, message: Message):
    try:
        credentials = None
        # Load credentials from token file
        with open(TOKEN_FILE, "r") as token:
            credentials = token.read()
        
        # Build the Google Drive API service
        service = build("drive", "v3", credentials=credentials)
        
        # Set the metadata for the file
        file_metadata = {
            "name": file_path.split("/")[-1],
            "parents": [FOLDER_ID]
        }
        
        # Create a media file upload object
        media = MediaFileUpload(file_path, resumable=True)
        request = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        )
        
        # Start the file upload with a progress bar
        progress_message = await message.edit(f"📤 <b>Uploading file</b> <code>{file_path}</code> to Google Drive...")
        progress = 0
        previous_progress = 0
        start_time = time.time()
        while progress < 100:
            _, progress = request.next_chunk()
            if progress:
                current_progress = int(progress.progress() * 100)
                if current_progress > previous_progress:
                    elapsed_time = round(time.time() - start_time)
                    await progress_message.edit(f"📤 <b>Uploading file</b> <code>{file_path}</code> to Google Drive...\n\nProgress: {current_progress}%\nElapsed Time: {elapsed_time}s")
                    previous_progress = current_progress
            await asyncio.sleep(5)
        
        # Get the file ID after upload completion
        response = request.execute()
        file_id = response.get("id")
        
        return file_id
    except Exception as e:
        return format_exc(e)


@Client.on_message(filters.command(["upload_to_drive"], prefix) & filters.me)
async def upload_to_drive_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit("🚫 <b>Please specify a file to upload.</b>")
        return
    
    file_path = message.command[1]
    
    try:
        file_id = await upload_file_to_drive(file_path, message)
        await message.edit(f"✅ <b>File uploaded to Google Drive!</b>\n\nFile ID: <code>{file_id}</code>")
    except Exception as e:
        await message.edit(f"❌ <b>Error occurred while uploading file to Google Drive:</b>\n<code>{format_exc(e)}</code>")


modules_help["upload_to_drive"] = {
    "upload_to_drive": "The module to upload a file from Telegram to Google Drive using the Drive API",
}
