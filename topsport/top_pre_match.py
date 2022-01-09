from bs4 import BeautifulSoup
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

            tmp.append([sport, league_name, event_date, home_name, away_name, href])

    return tmp
