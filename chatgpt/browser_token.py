import asyncio
import json
import platform
import os
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from utils.Logger import logger


class BrowserTokenRetriever:
    """Retrieves ChatGPT access token from browser session"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def get_browser_data_dir(self) -> str:
        """Get the default browser data directory based on OS"""
        system = platform.system().lower()
        home = os.path.expanduser("~")
        
        if system == "windows":
            return os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data")
        elif system == "darwin":  # macOS
            return os.path.join(home, "Library", "Application Support", "Google", "Chrome")
        elif system == "linux":
            return os.path.join(home, ".config", "google-chrome")
        else:
            raise Exception(f"Unsupported operating system: {system}")
    
    async def launch_browser(self) -> None:
        """Launch browser with existing user data"""
        playwright = await async_playwright().start()
        
        try:
            # Try to get user data directory
            user_data_dir = await self.get_browser_data_dir()
            
            # Launch browser with user data
            self.browser = await playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-bgsync",
                    "--disable-extensions-http-throttling",
                    "--disable-features=TranslateUI",
                    "--disable-ipc-flooding-protection",
                ]
            )
            
            # Create new page
            self.page = await self.browser.new_page()
            
        except Exception as e:
            logger.warning(f"Failed to launch browser with user data: {e}")
            # Fallback to regular browser launch
            browser = await playwright.chromium.launch(headless=True)
            self.context = await browser.new_context()
            self.page = await self.context.new_page()
    
    async def get_access_token(self) -> Optional[str]:
        """
        Retrieve access token from ChatGPT session
        Returns the access_token if successful, None otherwise
        """
        try:
            await self.launch_browser()
            
            # Navigate to ChatGPT auth session endpoint
            logger.info("Navigating to ChatGPT session endpoint...")
            response = await self.page.goto(
                "https://chatgpt.com/api/auth/session",
                wait_until="networkidle",
                timeout=30000
            )
            
            if not response:
                logger.error("Failed to navigate to session endpoint")
                return None
            
            # Check if we got a valid response
            if response.status != 200:
                logger.error(f"Session endpoint returned status {response.status}")
                return None
            
            # Get the response text
            session_data = await response.text()
            
            try:
                # Parse JSON response
                session_json = json.loads(session_data)
                
                # Extract access token
                access_token = session_json.get("accessToken")
                
                if access_token:
                    logger.info("Successfully retrieved access token from browser session")
                    return access_token
                else:
                    logger.warning("No access token found in session data")
                    return None
                    
            except json.JSONDecodeError:
                logger.error("Invalid JSON response from session endpoint")
                return None
            
        except Exception as e:
            logger.error(f"Error retrieving access token: {e}")
            return None
        
        finally:
            await self.cleanup()
    
    async def cleanup(self) -> None:
        """Clean up browser resources"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")


async def get_browser_access_token() -> Optional[str]:
    """
    Convenience function to get access token from browser
    Returns access_token string or None if failed
    """
    retriever = BrowserTokenRetriever()
    return await retriever.get_access_token()


# For testing purposes
async def main():
    token = await get_browser_access_token()
    if token:
        print(f"Access token retrieved: {token[:50]}...")
    else:
        print("Failed to retrieve access token")


if __name__ == "__main__":
    asyncio.run(main())