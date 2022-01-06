from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from bet365_helper import process_data
import datetime
import time

SPORT_DICT = {'Basketball': 18, 'Soccer': 1}


def monitor(sport='Basketball'):
    with sync_playwright() as p:
        # launch webdriver browser in headless mode
        browser = p.chromium.launch(headless=True, slow_mo=50)

        # create new page
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
        page = browser.new_page(user_agent=user_agent)

        # generate new url based on sport
        url = f"https://www.bet365.com/#/IP/B{SPORT_DICT[sport]}"

        # visit sport's page
        page.goto(url)

        # wait till page loads by clicking on a dummy element
        page.click('div[class="ovm-ClassificationHeader_Text "]')

        # scroll down
        page.keyboard.press("End")

        # iterate over time
        for i in range(30):
            # get page content for extracting data with bs4
            page_source = page.content()

            # convert to bs4 element
            soup = BeautifulSoup(page_source, "lxml")

            # generate file name
            record_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_name = f'bet365_{sport}_' + record_time[:10].replace('-', '_') + '.csv'

            # read data
            try:
                data = process_data(soup, sport=sport)
            except Exception as error_name:
                print(f'{error_name}')
                print('Odds were not read.')
            else:
                # write data to csv file
                with open(file_name, 'a', encoding='utf-8') as fd:
                    for line in data:
                        line = record_time + ',' + ','.join(line) + '\n'
                        fd.write(line)

            # take screenshot
            page.screenshot(path=f"bet365_status.png")

            # wait till next iteration
            time.sleep(20)

        # close browser after monitoring is finished
        browser.close()


# run monitoring script
if __name__ == '__main__':
    i = 1
    start_time = time.time()
    while i:
        try:
            monitor()
        except Exception as e:
            print(f'Error {e}')
            print("Interupted")

        duration = time.time() - start_time
        print(i, f'recording {duration / 60:.2f} minutes.')
        i += 1

