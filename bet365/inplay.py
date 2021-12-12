import asyncio
from playwright.async_api import async_playwright

SPORT_DICT = {'Basketball': 18, 'Soccer': 1}


async def monitor(sport='Basketball'):
    async with async_playwright() as p:

        # launch webdriver browser in headless mode
        browser = await p.chromium.launch(headless=True, slow_mo=50)

        # create new page
        page = await browser.new_page()

        # generate new url based on sport
        url = f"https://www.bet365.com/#/IP/B{SPORT_DICT[sport]}"

        # visit sport's page
        await page.goto(url)

        # wait till page loads by clicking on a dummy element
        await page.click('div[class="ovm-ClassificationHeader_Text "]')

        # get page content for extracting data with bs4
        # page_source = await page.content()

        # close browser after monitoring is finished
        await browser.close()

asyncio.run(monitor())
