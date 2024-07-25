import re
from playwright.async_api import async_playwright, Page

class BrowserAutomation:
    def __init__(self):
        self.browser = None
        self.page: Page = None
        self.playwright = None

    async def launch_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()

    async def navigate(self, url):
        await self.page.goto(url)
        await self.page.wait_for_load_state('networkidle')

    async def close_browser(self):
        await self.browser.close()
        await self.playwright.stop()

    async def fetch_page_content(self):
        if not self.page:
            raise AttributeError("Page is not initialized. Call launch_browser() and navigate() before fetch_page_content().")
        content = await self.page.content()
        return content

    @staticmethod
    def extract_field_name(name):
        """ Extracts the field name within brackets if present, otherwise returns the name itself. """
        match = re.search(r'\[(.*?)\]', name)
        return match.group(1) if match else name
