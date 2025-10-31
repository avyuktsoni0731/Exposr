import asyncio
import urllib.parse
from playwright.async_api import async_playwright

async def fetch_hibp_data(email: str):
    """Fetch breach data from HIBP unifiedsearch using Playwright."""
    encoded = urllib.parse.quote(email)
    url = f"https://haveibeenpwned.com/unifiedsearch/{encoded}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ))
        page = await context.new_page()
        
        response = await page.goto(url, wait_until="networkidle")
        if not response:
            print("❌ No response received.")
            await browser.close()
            return None

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            data = await response.json()
            await browser.close()
            return data
        else:
            text = await response.text()
            print("⚠️ Non-JSON response (blocked or error):", text[:200])
            await browser.close()
            return None
