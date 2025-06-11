from TikTokApi import TikTokApi
from yt_dlp import YoutubeDL
import asyncio
import os
from config import TEMP_DIR, OUTPUTS_DIR
from utils import proxy_retriever

ms_token = os.environ.get("ms_token", None)
ydl_opts = {
    'outtmpl': '%(uploader)s_%(id)s_%(timestamp)s.%(ext)s',
    'paths': {"home": "temp"}
}

async def trending_videos():
    async with TikTokApi() as api:
        # Retrieve and get proxy list
        # proxy_retriever.retrieve_proxy_list()
        # proxy_list = proxy_retriever.get_proxy_urls_from_file()
        
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False, browser="chromium")
        # Create a directory to store the videos if it doesn't exist
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(OUTPUTS_DIR, exist_ok=True)

        video_count = 0
        async for video in api.hashtag("memes").videos(count=3):
            try:
                print(f"Downloading video: {video.id}")
                video_url = f"https://www.tiktok.com/@{video.author.username}/video/{video.id}"
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                print(f"Downloaded {video.id}.mp4")
                video_count += 1
            except Exception as e:
                print(f"Error downloading video {video.id}: {e}")
        print(f"Finished downloading {video_count} trending videos.")

if __name__ == "__main__":
    asyncio.run(trending_videos())