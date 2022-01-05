from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
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
        for i in range(1):
            # get page content for extracting data with bs4
            page_source = page.content()

            # convert to bs4 element
            soup = BeautifulSoup(page_source, "lxml")

            # get all competitions
            comp = soup.findAll('div', {'class': 'ovm-Competition ovm-Competition-open'})

            # iterate over competitions
            for c in comp:
                league = c.find('div', {'class': 'ovm-CompetitionHeader_NameText'}).text

                # get events
                events = c.findAll('div', {'class': 'ovm-Fixture ovm-Fixture-media'})

                # iterate over events
                for event in events:
                    # team names
                    team_names = event.findAll('div', {'class': 'ovm-FixtureDetailsTwoWay_TeamName'})
                    if team_names:
                        home_name, away_name = team_names[0].text, team_names[1].text
                    else:
                        home_name, away_name = '', ''

                    # game status
                    game_status = soup.find('div', {"class": 'ovm-FixtureDetailsTwoWay_PeriodWrapper'})

                    # scores
                    pts_home = soup.find('div', {'class': 'ovm-StandardScores_TeamOne'}).text
                    pts_away = soup.find('div', {'class': 'ovm-StandardScores_TeamOne'}).text

                    # get all markets
                    markets = event.findAll('div', {'class': 'ovm-Market'})

                    # AH line
                    ah = markets[0].findAll('div', {'class': 'ovm-ParticipantStackedCentered gl-Participant_General'})
                    if ah:
                        ah_line = ah[0].find('span', {'class': 'ovm-ParticipantStackedCentered_Handicap'}).text
                        ah_home = ah[0].find('span', {'class': 'ovm-ParticipantStackedCentered_Odds'}).text
                        ah_away = ah[1].find('span', {'class': 'ovm-ParticipantStackedCentered_Odds'}).text
                    else:
                        ah_line, ah_home, ah_away = '', '', ''

                    # OU line
                    ou = markets[1].findAll('div', {'class': 'ovm-ParticipantStackedCentered gl-Participant_General'})
                    if ou:
                        ou_line = ou[0].find('span', {'class': 'ovm-ParticipantStackedCentered_Handicap'}).text
                        ou_over = ou[0].find('span', {'class': 'ovm-ParticipantStackedCentered_Odds'}).text
                        ou_under = ou[1].find('span', {'class': 'ovm-ParticipantStackedCentered_Odds'}).text
                    else:
                        ou_line, ou_over, ou_under = '', '', ''

                    # money line
                    ml = markets[2].findAll('div', {'class': 'ovm-ParticipantOddsOnly gl-Participant_General'})
                    if ml:
                        ml_home = ml[0].find('span', {'class': 'ovm-ParticipantOddsOnly_Odds'}).text
                        ml_away = ml[1].find('span', {'class': 'ovm-ParticipantOddsOnly_Odds'}).text
                    else:
                        ml_home, ml_away = '', ''

                    print([league, home_name, away_name,
                           game_status.text,
                           pts_home, pts_away,
                           ah_line, ah_home, ah_away,
                           ou_line, ou_over, ou_under,
                           ml_home, ml_away])

            # take screenshot
            page.screenshot(path=f"bet365_status.png")

            # wait till next iteration
            time.sleep(20)

        # close browser after monitoring is finished
        browser.close()


# run monitoring script
if __name__ == '__main__':
    monitor()
