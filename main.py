from pyrogram import Client, filters
import re
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("music_tag_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def extract_artist_hashtags(artist: str):
    if not artist:
        return []

    separators = ['&', 'ft.', 'ft', 'Ft.', 'Ft', 'feat', 'Feat.', 'Feat']
    pattern = '|'.join(map(re.escape, separators))
    parts = re.split(pattern, artist, flags=re.IGNORECASE)

    hashtags = []
    for part in parts:
        tag = part.strip().replace(" ", "_")
        if tag:
            hashtags.append(f"#{tag}")
    return hashtags

@app.on_message(filters.channel & filters.audio)
async def on_audio(client, message):
    audio = message.audio
    artist = audio.performer  # اینجا تغییر اصلیه

    hashtags = extract_artist_hashtags(artist)
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
