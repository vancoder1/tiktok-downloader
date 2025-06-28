from yt_dlp import YoutubeDL
import os
from loguru import logger

# Common YDL options template
BASE_YDL_OPTS = {
    'outtmpl': '%(uploader)s_%(id)s_%(timestamp)s.%(ext)s',
    'quiet': True, # Suppress ytdl output unless errors
    'noplaylist': True, # Ensure only single video is downloaded if URL could be a playlist
    'paths': {"home": "temp"} # This will be updated dynamically
}

def _get_ydl_opts(output_dir: str):
    """Helper to configure ydl_opts for a specific download."""
    opts = BASE_YDL_OPTS.copy()
    opts['outtmpl'] = os.path.join(output_dir, '%(uploader)s_%(id)s_%(timestamp)s.%(ext)s')
    opts['paths'] = {"home": output_dir} # Use output_dir for temporary storage as well
    return opts

async def download_from_hashtag(api, hashtag: str, count: int, output_dir: str):
    logger.info(f"Attempting to download {count} videos for hashtag: #{hashtag}")
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = _get_ydl_opts(output_dir)
    
    downloaded_count = 0
    try:
        async for video_data in api.hashtag(hashtag).videos(count=count):
            video_url = f"https://www.tiktok.com/@{video_data.author.username}/video/{video_data.id}"
            logger.debug(f"Downloading video by URL: {video_url} (ID: {video_data.id})")
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                logger.success(f"Successfully downloaded video ID: {video_data.id} to {output_dir}")
                downloaded_count += 1
            except Exception as e:
                logger.error(f"Failed to download video ID {video_data.id} from {video_url}: {e}")
    except Exception as e:
        logger.error(f"Error fetching videos for hashtag #{hashtag}: {e}")
        raise # Re-raise to be caught by CLI
    return downloaded_count

async def download_from_user(api, username: str, count: int, output_dir: str):
    logger.info(f"Attempting to download {count} videos for user: @{username}")
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = _get_ydl_opts(output_dir)

    downloaded_count = 0
    try:
        async for video_data in api.user(username).videos(count=count):
            video_url = f"https://www.tiktok.com/@{video_data.author.username}/video/{video_data.id}"
            logger.debug(f"Downloading video by URL: {video_url} (ID: {video_data.id})")
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                logger.success(f"Successfully downloaded video ID: {video_data.id} to {output_dir}")
                downloaded_count += 1
            except Exception as e:
                logger.error(f"Failed to download video ID {video_data.id} from {video_url}: {e}")
    except Exception as e:
        logger.error(f"Error fetching videos for user @{username}: {e}")
        raise
    return downloaded_count

async def download_from_url(api, video_url: str, output_dir: str):
    logger.info(f"Attempting to download video from URL: {video_url}")
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = _get_ydl_opts(output_dir)

    try:
        # For a single URL, TikTokApi might not be strictly needed just for ytdl,
        # but if you wanted to fetch metadata first via TikTokApi, you could.
        # Here, we'll assume ytdl handles the direct URL download.
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        logger.success(f"Successfully downloaded video from {video_url} to {output_dir}")
        return 1 # Downloaded one video
    except Exception as e:
        logger.error(f"Failed to download video from URL {video_url}: {e}")
        raise
    return 0

async def download_trending_videos(api, count: int, output_dir: str):
    logger.info(f"Attempting to download {count} trending videos.")
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = _get_ydl_opts(output_dir)

    downloaded_count = 0
    try:
        async for video_data in api.trending().videos(count=count):
            video_url = f"https://www.tiktok.com/@{video_data.author.username}/video/{video_data.id}"
            logger.debug(f"Downloading video by URL: {video_url} (ID: {video_data.id})")
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                logger.success(f"Successfully downloaded video ID: {video_data.id} to {output_dir}")
                downloaded_count += 1
            except Exception as e:
                logger.error(f"Failed to download video ID {video_data.id} from {video_url}: {e}")
    except Exception as e:
        logger.error(f"Error fetching trending videos: {e}")
        raise
    return downloaded_count