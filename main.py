from pyrogram import Client, filters
import re
import os

# گرفتن مقادیر از متغیرهای محیطی
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("music_tag_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def extract_artists_from_title(title: str):
    separators = ['&', 'ft.', 'ft', 'Ft.', 'Ft']
    pattern = '|'.join(map(re.escape, separators))
    parts = re.split(pattern, title, flags=re.IGNORECASE)
    artists = []
    for part in parts:
        name = part.strip().lower().replace(" ", "_")
        if name:
            artists.append(f"#{name}")
    return artists

@app.on_message(filters.channel & filters.audio)
async def tag_artist(client, message):
    audio = message.audio
    title = audio.title or audio.file_name
    if not title:
        return
    hashtags = extract_artists_from_title(title)
    if not hashtags:
        return
    artist_line = "Artist : " + ", ".join(hashtags)
    old_caption = message.caption or ""
    if artist_line in old_caption:
        return
    new_caption = f"{old_caption.strip()}\n{artist_line}" if old_caption else artist_line
    try:
        await message.edit_caption(new_caption)
    except Exception as e:
        print(f"× Error editing caption: {e}")

app.run()
