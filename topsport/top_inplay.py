import time

from helper_functions import get_odds
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import datetime


SPORT_DICT = {'Krepšinis': 'b_', 'Futbolas': 'f_', 'Ledo ritulys': 'h_'}


class OddsportalPage:
    def __init__(self, page, sport):
        self.sport = sport
        self.page = page

        # go to Topsport page
        self.page.goto("https://www.topsport.lt/lazybos-gyvai")

        # close popup
        self.page.click("button[class='Cookie__button']")

        # wait till menu loads
        self.page.frame(name="sportsFrame").wait_for_selector("div[class='rc-tabs-nav rc-tabs-nav-animated']")

        # click understand rules button
        self.page.click("text='Supratau, neberodyti daugiau.'")

    def select(self):
        """
        This functions selects specific sport menu.
        :return: None
        """
        # click sport menu item
        if self.page.frame(name="sportsFrame").is_visible(f"text='{self.sport}'"):
            self.page.frame(name="sportsFrame").click(f"text='{self.sport}'")
        else:
            # click next button if sport not found
            self.page.frame(name="sportsFrame").click(".rc-tabs-tab-next")
            # click sport menu item
            if self.page.frame(name="sportsFrame").is_visible(f"text='{self.sport}'"):
                self.page.frame(name="sportsFrame").click(f"text='{self.sport}'")
            else:
                print(f'{self.sport} is not available')

        # wait till matches are loaded
        self.page.frame(name="sportsFrame").wait_for_selector(f"div[class=MatchList__Header]")

    def open_all_markets(self):
        """
        This function checks whatever more events are available on page.
        :return: None
        """
        # check if more matches are available
        while self.page.frame(name="sportsFrame").is_visible("text='Rodyti daugiau'"):
            self.page.frame(name="sportsFrame").click("text='Rodyti daugiau'")

    def record_odds(self):
        """
        This function saves odds and scores to .csv file.
        :return: None
        """

        # get page source and generate soup
        page_source = self.page.frame(name="sportsFrame").content()
        soup = BeautifulSoup(page_source, "lxml")

        # generate file name
        record_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = f'{SPORT_DICT.get(self.sport)}' + record_time[:10].replace('-', '_') + '.csv'

        # get odds
        try:
            data = get_odds(soup, sport=self.sport)
        except Exception as error_name:
            print(f'{error_name}')
            print(f'Odds were not read for {self.sport}')
        else:
            # write data to csv file
            with open(file_name, 'a', encoding='utf-8') as fd:
                for line in data:
                    line = record_time + ',' + ','.join(line) + '\n'
                    fd.write(line)

        # take screenshot
        self.page.screenshot(path=f"{SPORT_DICT[self.sport]}status.png")


def monitor():
    """
    This function monitors topsport inplay odds for specific sport type.
    :return: None
    """
    with sync_playwright() as p:

        # launch webdriver browser in headless mode
        browser = p.chromium.launch(headless=False, slow_mo=50)

        # create new pages
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'

        # create basketball page Object
        page_b = browser.new_page(user_agent=user_agent)
        page_b = OddsportalPage(page_b, 'Krepšinis')

        # create ice-hockey page Object
        page_h = browser.new_page(user_agent=user_agent)
        page_h = OddsportalPage(page_h, 'Ledo ritulys')

        # create football page Object
        page_f = browser.new_page(user_agent=user_agent)
        page_f = OddsportalPage(page_f, 'Futbolas')

        # select specific sport
        page_b.select()
        page_h.select()
        page_f.select()

        # run loop for 30 min, when reboot
        for m in range(30):

            start = time.time()

            # check if more matches are available
            page_b.open_all_markets()
            page_h.open_all_markets()
            page_f.open_all_markets()

            # record odds
            page_b.record_odds()
            page_h.record_odds()
            page_f.record_odds()

            # sleep if duration was less than 30 secs
            dur = time.time() - start
            if dur < 30:
                time.sleep(int(30 - dur))

            # select sports after reloading
            page_b.select()
            page_h.select()
            page_f.select()

        # close browser
        browser.close()


# run app forever
if __name__ == '__main__':

    # mark when script was started
    start_time = time.time()
    while True:
        try:
            monitor()
        except Exception as e:
            print(f'Error {e}')
            print("Interupted")

        duration = time.time() - start_time
        # return duration
        print(f'recording {duration/60:.2f} minutes.')

