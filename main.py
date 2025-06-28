import click
import asyncio
import os
from loguru import logger # Import logger directly

# Import your separated logic
from tiktok import (
    TikTokClient,
    download_from_hashtag,
    download_from_user,
    download_from_url,
    download_trending_videos
)
# from tiktok.exceptions import TikTokError # If using custom exceptions

# proxy_retriever is not used in the provided main.py, but kept if needed elsewhere
# from utils import proxy_retriever
from utils.logging_config import setup_logging
from config import OUTPUTS_DIR, TEMP_DIR # PROXY_LIST_FILE, DEBUG_MODE not used here

# --- Common Click options ---
output_dir_option = click.option(
    '--output-dir', 'output_directory',
    default=TEMP_DIR, # Changed default to TEMP_DIR
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    show_default=True,
    help='Output directory for videos. Defaults to temporary directory.'
)
count_option = click.option(
    '--count', type=int, default=10, show_default=True,
    help='Max videos to download (for hashtag, user, trending).'
)


@click.group()
@click.option(
    '--headless/--no-headless',
    default=False,
    show_default=True,
    help="Run the automated browser in headless mode (no visible UI)."
)
@click.option(
    '--browser',
    default='chromium',
    type=click.Choice(['chromium', 'firefox', 'webkit'], case_sensitive=False),
    show_default=True,
    help="Specify the browser engine (e.g., chromium, firefox) for TikTok interactions."
)
@click.pass_context
def cli(ctx, headless: bool, browser: str):
    """
    \b
    TikTok Video Downloader

    Download TikTok videos by hashtag, user, URL, or trending feeds.

    Usage: COMMAND [OPTIONS]
    Example: by-hashtag --help
    """
    ctx.ensure_object(dict)
    setup_logging()
    _ms_token = os.environ.get("ms_token", None)

    ctx.obj['ms_token'] = _ms_token
    ctx.obj['tiktok_headless'] = headless
    ctx.obj['tiktok_browser'] = browser
    logger.debug(f"CLI context: ms_token, headless: {headless}, browser: {browser}")


async def _run_tiktok_operation(ctx, operation_coro, success_message_template):
    """Helper to run async TikTok operations and handle client."""
    ms_token = ctx.obj['ms_token']
    headless = ctx.obj['tiktok_headless']
    browser = ctx.obj['tiktok_browser']

    try:
        async with TikTokClient(ms_token=ms_token, headless=headless, browser=browser) as api_client:
            downloaded_count = await operation_coro(api_client)

        if downloaded_count > 0:
            message = success_message_template.format(count=downloaded_count)
            logger.info(message)
            click.echo(click.style(message, fg="green"))
        elif downloaded_count == 0:
            logger.info("No videos were downloaded for the given criteria.")
            click.echo("No videos were downloaded. This could be due to the criteria, or no new videos matching.")
        # Negative counts are not expected from current downloaders.
    except Exception as e:
        logger.error(f"An unexpected error occurred during the TikTok operation: {e}", exc_info=True)
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"), err=True)
        ctx.exit(1)

@cli.command("by-hashtag")
@click.option('--hashtag', required=True, help='The TikTok hashtag to search for (e.g., "catvideos", not "#catvideos").')
@count_option
@output_dir_option
@click.pass_context
def tiktok_by_hashtag(ctx, hashtag: str, count: int, output_directory: str):
    """Download videos by hashtag."""
    logger.info(f"CLI: Download by hashtag '{hashtag}', count: {count}, output: '{output_directory}'")

    async def operation(api_client):
        return await download_from_hashtag(
            api_client, hashtag, count, output_directory
        )
    asyncio.run(_run_tiktok_operation(ctx, operation, f"Successfully downloaded {{count}} video(s) for hashtag #{hashtag}."))

@cli.command("by-user")
@click.option('--username', required=True, help='The TikTok username whose videos you want to download (e.g., "tiktok", not "@tiktok").')
@count_option
@output_dir_option
@click.pass_context
def tiktok_by_user(ctx, username: str, count: int, output_directory: str):
    """Download videos by user."""
    logger.info(f"CLI: Download by user '@{username}', count: {count}, output: '{output_directory}'")
    async def operation(api_client):
        return await download_from_user(
            api_client, username, count, output_directory
        )
    asyncio.run(_run_tiktok_operation(ctx, operation, f"Successfully downloaded {{count}} video(s) for user @{username}."))

@cli.command("by-url")
@click.option('--url', 'video_url', required=True, help='The complete URL of the TikTok video you want to download.')
@output_dir_option
@click.pass_context
def tiktok_by_url(ctx, video_url: str, output_directory: str):
    """Download a single video by URL."""
    logger.info(f"CLI: Download by URL '{video_url}', output: '{output_directory}'")
    async def operation(api_client):
        return await download_from_url(
            api_client, video_url, output_directory
        )
    # Adjust success message for single download
    asyncio.run(_run_tiktok_operation(ctx, operation, "Successfully downloaded 1 video from the URL."))


@cli.command("trending")
@count_option
@output_dir_option
@click.pass_context
def tiktok_trending(ctx, count: int, output_directory: str):
    """Download trending videos."""
    logger.info(f"CLI: Download trending, count: {count}, output: '{output_directory}'")
    async def operation(api_client):
        return await download_trending_videos(
            api_client, count, output_directory
        )
    asyncio.run(_run_tiktok_operation(ctx, operation, "Successfully downloaded {count} trending video(s)."))

if __name__ == "__main__":
    cli()