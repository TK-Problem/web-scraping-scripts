import time

from helper_functions import get_odds
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import datetime


SPORT_DICT = {'Krepšinis': 'b_', 'Futbolas': 'f_'}


def monitor(sport='Krepšinis', time_count=30):
    """
    This function monitors topsport inplay odds for specific sport type.
    :param sport: str
    :param time_count: int
    :return: None
    """
    with sync_playwright() as p:
        # launch webdriver browser in headless mode
        browser = p.chromium.launch(headless=True, slow_mo=50)

        # create new page
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
        page = browser.new_page(user_agent=user_agent)

        # go to topsport page
        page.goto("https://www.topsport.lt/lazybos-gyvai")

        # close popup
        page.click("button[class='Cookie__button']")

        # wait till menu loads
        page.frame(name="sportsFrame").wait_for_selector("div[class='rc-tabs-nav rc-tabs-nav-animated']")

        # click sport menu item
        if page.frame(name="sportsFrame").is_visible(f'text={sport}'):
            page.frame(name="sportsFrame").click(f'text={sport}')
        else:
            print(f'{sport} is not available')

        # wait till matches are loaded
        page.frame(name="sportsFrame").wait_for_selector(f"div[class=MatchList__Header]")

        # iterate over time
        for m in range(time_count):

            # get page source and generate soup
            page_source = page.frame(name="sportsFrame").content()
            page.screenshot(path="example.png")
            soup = BeautifulSoup(page_source, "lxml")

            # generate file name
            record_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_name = f'{SPORT_DICT.get(sport)}' + record_time[:10].replace('-', '_') + '.csv'

            # get odds
            data = get_odds(soup, sport=sport)

            # write data to csv file
            with open(file_name, 'a', encoding='utf-8') as fd:
                for line in data:
                    line = record_time + ',' + ','.join(line) + '\n'
                    fd.write(line)

            # reload page
            page.reload()

            # sleep
            time.sleep(20)

            # click sport menu item
            if page.frame(name="sportsFrame").is_visible(f'text={sport}'):
                page.frame(name="sportsFrame").click(f'text={sport}')
            else:
                print(f'{sport} is not available')

            # take screenshot
            page.screenshot(path="example.png")

            # wait till matches are loaded
            page.frame(name="sportsFrame").wait_for_selector(f"div[class=MatchList__Header]")

        # close browser
        browser.close()


# run app
if __name__ == '__main__':
    monitor('Futbolas')
