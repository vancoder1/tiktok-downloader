from TikTokApi import TikTokApi
from loguru import logger

class TikTokClient:
    def __init__(self, ms_token: str, headless: bool = False, browser: str = "chromium"):
        self.ms_token = ms_token
        self.headless = headless
        self.browser = browser
        self._api = None

    async def __aenter__(self):
        """Initializes the TikTokApi session."""
        if not self.ms_token:
            logger.error("MS Token is not provided for TikTokClient.")
            raise ValueError("MS Token is required to initialize TikTokClient.")
        
        self._api = TikTokApi(headless=self.headless, browser_name=self.browser)
        logger.debug(f"Creating TikTok session with token (first 5 chars): {self.ms_token[:5]}...")
        await self._api.create_sessions(ms_tokens=[self.ms_token], num_sessions=1, sleep_after=3)
        logger.info("TikTok session created successfully.")
        return self._api # Return the underlying api instance for direct use

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the TikTokApi session."""
        if self._api:
            logger.debug("Closing TikTok session.")
            # TikTokApi's __aexit__ handles cleanup, so just ensure it's called
            await self._api.__aexit__(exc_type, exc_val, exc_tb) 
        if exc_type:
            logger.error(f"TikTokClient exited with an error: {exc_val}", exc_info=(exc_type, exc_val, exc_tb))