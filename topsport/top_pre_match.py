from bs4 import BeautifulSoup
import datetime
import requests


def get_today_events():
    """
    This function returns list of all today games.
    :return: lst
    """
    # load available pages
    urls = ['https://www.topsport.lt/lazybos-siandien/futbolas',
            'https://www.topsport.lt/lazybos-siandien/krepsinis',
            'https://www.topsport.lt/lazybos-siandien/tenisas']

    # for testing
    # urls = ['https://www.topsport.lt/lazybos-siandien/tenisas']

    # tmp.list to store data
    tmp_data = list()

    # iterate over all supplied markets
    for url in urls:
        # load HTML dom and convert to bs4 element
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        # get sport name from url
        sport = url.split('/')[-1]

        # process data
        tmp_data += top_market_data(soup, sport)

    return tmp_data


def top_market_data(soup, sport):
    """
    This function process soup element to extract event urls.
    :param soup: bs4 element
    :param sport: str
    :return: list
    """
    # get leagues
    blocks = soup.findAll('div', {'class': 'prelive-list-section'})

    # temp.list to save records
    tmp = list()

    # generate timestamp data was collected
    record_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # iterate over blocks
    for block in blocks:

        # get league name
        league_name = block.h5.text.strip()

        # find all events
        events = block.findAll('div', {'class': 'prelive-list-itemscope'})

        # iterate over all events
        for event in events:

            # get event date
            event_date = event.find('div', {'class': 'mt-2 mt-sm-0'}).findAll('div', recursive=False)
            if event_date:
                event_date = event_date[0].findAll('span')[-1].text

            # team names
            t_names = event.findAll('div', {'class': 'prelive-list-league-choice-title d-flex align-items-center'})
            if len(t_names) > 1:
                home_name, away_name = t_names[0].text.strip(), t_names[-1].text.strip()
            else:
                home_name, away_name = '', ''

            # get event url
            href = event.find('meta', {'itemprop': 'url'})
            if href:
                href = href['content']

            tmp.append([record_time, sport, league_name, event_date, home_name, away_name, href])

    return tmp


MARKET_DICT = {'Kas laimės (1x2)': '1x2',
               'Rungtynių nugalėtojas (įskaitant pratęsimą)': 'ML',
               'Kas laimės': 'ML',
               'Įvarčių kiekis per rungtynes': 'OU',
               'Abiejų komandų pelnyti taškai (įskaitant pratęsimą)': 'OU',
               'Sužaistų geimų kiekis mače': 'OU',
               'Pranašumas 2': 'AH',
               'Pranašumas (įskaitant pratęsimą)': 'AH'}


def top_event_odds(url):
    """
    This function returns available odds.
    :param url: str
    :return: list
    """
    # load HTML dom and convert to bs4 element
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    # generate timestamp data was collected
    record_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # long class names
    _class_name_1 = 'd-flex align-items-center justify-content-between pl-2 pl-md-0 h-fs15 h-lh1_2'
    _class_name_2 = 'prelive-list-league-rate ml-1 h-font-secondary h-fs17 h-fw500'

    # create temp. list to store data
    tmp_list = list()

    # get all markets
    markets = soup.findAll('div', {'class': 'prelive-list-game-item js-prelive-event-row mb-4 h-rel'})
    for market in markets:
        # identify market type
        bet_type = market.find('div', {'class': _class_name_1}).text.strip()

        # check if market is known
        if bet_type in MARKET_DICT.keys():

            # convert bet_type
            bet_type = MARKET_DICT[bet_type]

            # find all odds
            odds = market.findAll('span', {'class': _class_name_2})

            # get 1x2 prices
            if bet_type == '1x2':
                # record data
                tmp_list.append([record_time, url, bet_type, 'Home', odds[0].text.replace(',', '.')])
                tmp_list.append([record_time, url, bet_type, 'Draw', odds[1].text.replace(',', '.')])
                tmp_list.append([record_time, url, bet_type, 'Away', odds[-1].text.replace(',', '.')])

            # get ML prices
            if bet_type == 'ML':
                # record data
                tmp_list.append([record_time, url, bet_type, 'Home', odds[0].text.replace(',', '.')])
                tmp_list.append([record_time, url, bet_type, 'Draw', odds[-1].text.replace(',', '.')])

            # get OU prices
            elif bet_type == 'OU':
                for i in range(len(odds)//2):
                    # get odds
                    under_odds = odds[i*2].text.replace(',', '.')
                    over_odds = odds[i*2 + 1].text.replace(',', '.')
                    # get OU line
                    ou_line = float(odds[i*2].parent.parent.strong.text.replace(',', '.'))
                    # record data
                    tmp_list.append([record_time, url, f"OU{ou_line:.1f}", 'Over', over_odds])
                    tmp_list.append([record_time, url, f"OU{ou_line:.1f}", 'Under', under_odds])

            # get AH prices
            elif bet_type == 'AH':
                for i in range(len(odds) // 2):
                    # get odds
                    home_odds = odds[i * 2].text.replace(',', '.')
                    away_odds = odds[i * 2 + 1].text.replace(',', '.')
                    # get AH lines
                    ah_home = float(odds[i * 2].parent.parent.strong.text.replace(',', '.'))
                    ah_away = float(odds[i * 2 + 1].parent.parent.strong.text.replace(',', '.'))

                    # define line
                    if ah_away != 0:
                        ah_line = -1 * ah_away
                    else:
                        ah_line = ah_home

                    # record data
                    tmp_list.append([record_time, url, f"AH{ah_line:.1f}", 'Home', home_odds])
                    tmp_list.append([record_time, url, f"AH{ah_line:.1f}", 'Away', away_odds])

    return tmp_list


