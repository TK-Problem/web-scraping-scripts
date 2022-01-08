import time

from helper_functions import get_odds
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import datetime


SPORT_DICT = {'Krepšinis': 'b_', 'Futbolas': 'f_', 'Ledo ritulys': 'h_'}


class OddsportalPage:
    def __init__(self, page):
        self.page = page


def monitor(sport='Krepšinis'):
    """
    This function monitors topsport inplay odds for specific sport type.
    :param sport: str
    :return: None
    """
    with sync_playwright() as p:
        # launch webdriver browser in headless mode
        browser = p.chromium.launch(headless=False, slow_mo=50)

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
        if page.frame(name="sportsFrame").is_visible(f"text='{sport}'"):
            page.frame(name="sportsFrame").click(f"text='{sport}'")
        else:
            # click next button if sport not found
            page.frame(name="sportsFrame").click(".rc-tabs-tab-next")
            # click sport menu item
            if page.frame(name="sportsFrame").is_visible(f"text='{sport}'"):
                page.frame(name="sportsFrame").click(f"text='{sport}'")
            else:
                print(f'{sport} is not available')

        # wait till matches are loaded
        page.frame(name="sportsFrame").wait_for_selector(f"div[class=MatchList__Header]")

        # click understand rules button
        page.click("text='Supratau, neberodyti daugiau.'")

        # iterate over time
        for m in range(2):

            # check if more matches are available
            while page.frame(name="sportsFrame").is_visible("text=Rodyti daugiau"):
                page.frame(name="sportsFrame").click("text=Rodyti daugiau")

            # get page source and generate soup
            page_source = page.frame(name="sportsFrame").content()
            soup = BeautifulSoup(page_source, "lxml")

            # generate file name
            record_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_name = f'{SPORT_DICT.get(sport)}' + record_time[:10].replace('-', '_') + '.csv'

            # get odds
            try:
                data = get_odds(soup, sport=sport)
            except Exception as error_name:
                print(f'{error_name}')
                print('Odds were not read.')
            else:
                # write data to csv file
                with open(file_name, 'a', encoding='utf-8') as fd:
                    for line in data:
                        line = record_time + ',' + ','.join(line) + '\n'
                        fd.write(line)

            # reload page every 10th time
            if (m+1) % 10 == 0:
                page.reload()

            # take screenshot
            page.screenshot(path=f"{SPORT_DICT[sport]}status.png")

            # sleep
            time.sleep(20)

            # click sport menu item
            if page.frame(name="sportsFrame").is_visible(f"text='{sport}'"):
                page.frame(name="sportsFrame").click(f"text='{sport}'")
            else:
                # click next button if sport not found
                page.frame(name="sportsFrame").click(".rc-tabs-tab-next")
                # click sport menu item
                if page.frame(name="sportsFrame").is_visible(f"text='{sport}'"):
                    page.frame(name="sportsFrame").click(f"text='{sport}'")
                else:
                    print(f'{sport} is not available')

            # wait till matches are loaded
            page.frame(name="sportsFrame").wait_for_selector(f"div[class=MatchList__Header]")

        # close browser
        browser.close()


# run app
if __name__ == '__main__':
    # _sport = input('Įveskite sporto šaką: ')
    # while _sport not in SPORT_DICT:
    #     _sport = input('Įveskite sporto šaką: ')

    # Click .rc-tabs-tab-next
    # page.frame(name="sportsFrame").click(".rc-tabs-tab-next")

    _sport = 'Ledo ritulys'

    i = 1
    start_time = time.time()
    while i:
        try:
            monitor(_sport)
        except Exception as e:
            print(f'Error {e}')
            print("Interupted")

        duration = time.time() - start_time
        print(i, f'recording {duration/60:.2f} minutes.')
        i += 1
