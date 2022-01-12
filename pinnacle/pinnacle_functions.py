import requests


# sport dictonary
SPORT_DICT = {4: 'Basketball', 29: 'Soccer', 19: 'Hockey', 33: 'Tennis'}

# create user agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"


def convert_odds(usa_odds):
    """
    This function converts usa odds to european.
    e.g. +110 to 2.1, or -200 to 1.5.
    :param usa_odds: int or float
    :return:
    """
    if usa_odds < 0:
        return round(1 - (100/usa_odds), 3)
    else:
        return round(1 + (usa_odds/100), 3)


def get_pinna_matches(x_api_key, x_device_uuid):
    """
    This functions scrapes info about markets.
    :param x_api_key: str
    :param x_device_uuid: str
    :return: list
    """

    # temp list to store data
    tmp_lst = list()

    # iterate over sport types
    for sport_id in [4, 29, 19]:
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/matchups"
        # request for json file
        r = requests.get(url, timeout=15, headers={"X-API-Key": x_api_key,
                                                   "X-Device-UUID": x_device_uuid,
                                                   "User-Agent": USER_AGENT})

        # convert to json
        rows = r.json()

        # iterate over events
        for row in rows:

            # select league
            league = row['league']['name']

            # select market participants
            participants = row['participants']

            # take markets with only 2 participants
            if len(participants) == 2:

                # select only games with home and away teams
                if participants[0]['alignment'] == 'home':

                    # match start time
                    start_time = row['startTime'][:-1].replace('T', ' ')

                    # get match ID
                    match_id = row['id']

                    # add data to list
                    tmp_lst.append([SPORT_DICT[sport_id], league,
                                    participants[0]['name'], participants[1]['name'],
                                    start_time, match_id])

    return tmp_lst


def get_pinna_odds(x_api_key, x_device_uuid):
    """
    This function scrapes main markets odds. Returns 2 lists with
        * 2 outcome markets,
        * 3 outcome markets.
    :param x_api_key: str
    :param x_device_uuid: str
    :return: list, list
    """
    # temp. list to store data for 2 and 3 outcome odds
    odds_2 = list()
    odds_3 = list()

    # iterate over sports
    for sport_id in [4, 29, 19]:
        # generate url
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/markets/straight?primaryOnly=false"

        # add timeout exception if odds are not loaded within 15 secs.
        try:
            r = requests.get(url, timeout=15, headers={"X-API-Key": x_api_key,
                                                       "X-Device-UUID": x_device_uuid,
                                                       "User-Agent": USER_AGENT})

        # capture exception
        except Exception as e:
            print(f'{e}')
            print(f"{SPORT_DICT[sport_id]} odds were not loaded.")
            break
        else:
            # convert to json
            rows = r.json()

        # iterate over markets
        for row in rows:
            # get data from
            pinna_id = row['matchupId']
            period = row['period']
            bet_type = row['type']

            # select prices
            prices = row['prices']

            # select 2-outcome markets
            if len(prices) == 2 and bet_type in ['moneyline', 'spread', 'total']:
                # select line
                if bet_type in ['total', 'spread']:
                    bet_type += f"{prices[0]['points']}"

                odds_2.append([pinna_id, SPORT_DICT[sport_id], period, bet_type,
                               convert_odds(prices[0]['price']), convert_odds(prices[-1]['price'])])

            # select 3-outcome markets
            if len(prices) == 3:
                odds_3.append([pinna_id, SPORT_DICT[sport_id], period, bet_type,
                               convert_odds(prices[0]['price']),
                               convert_odds(prices[2]['price']),
                               convert_odds(prices[1]['price'])])

    return odds_2, odds_3

