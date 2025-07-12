import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
import os
import subprocess

API_TOKEN = "7793678424:AAE2QXy6PGX5HpLtQhAQFTPvN9pW2_rI-x0"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler()
async def send_movie(message: types.Message):
    movie_name = message.text.strip()
    await message.reply("🔍 جاري البحث عن الفيلم...")

    search_url = f"https://yts.mx/api/v2/list_movies.json?query_term={movie_name}"
    try:
        res = requests.get(search_url).json()
        if res["data"]["movie_count"] == 0:
            await message.reply("❌ لم أجد هذا الفيلم.")
            return

        movie = res["data"]["movies"][0]
        title = movie["title"]
        torrent_url = movie["torrents"][0]["url"]
        quality = movie["torrents"][0]["quality"]

        await message.reply(f"🎬 {title} ({quality})")
await message.reply("⬇️ جاري التحميل...")

subprocess.run(["aria2c", torrent_url, "-d", "downloads"], check=True)

for file in os.listdir("downloads"):
    if file.endswith(".mp4") or file.endswith(".mkv"):
        video_path = os.path.join("downloads", file)
        with open(video_path, 'rb') as video:
            await bot.send_video(message.chat.id, video, caption=f"🎬 {title} ({quality})")
        os.remove(video_path)
        break
else:
    await message.reply("⚠️ لم أجد ملف فيديو داخل التورنت.")

    except Exception as e:
        await message.reply("❌ حدث خطأ أثناء التحميل أو الرفع.")
        print(str(e))

if __name__ == '__main__':
    os.makedirs("downloads", exist_ok=True)
    executor.start_polling(dp)
