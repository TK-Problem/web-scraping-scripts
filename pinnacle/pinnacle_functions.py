import requests


def get_pinna_matches(x_api_key, x_device_uuid):
    """
    This functions info about markets.
    Abbreviations for markets.
    4- Basketball
    29- Soccer
    19- Hockey
    33- Tennis
    :param x_api_key: str
    :param x_device_uuid: str
    :return: list
    """
    # create user agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"

    # sport dictonary
    sport_dict = {4: 'Basketball', 29: 'Soccer', 19: 'Hockey', 33: 'Tennis'}

    # temp list to store data
    tmp_lst = list()

    # iterate over sport types
    for sport_id in [4, 29, 19, 33]:
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/matchups"
        # request for json file
        r = requests.get(url, timeout=15, headers={"X-API-Key": x_api_key,
                                                   "X-Device-UUID": x_device_uuid,
                                                   "User-Agent": user_agent})

        # convert to json
        rows = r.json()

        # iterate over events
        for row in rows:

            # select league
            league = row['league']['name']

            # count market participants
            participants = row['participants']
            if len(participants) == 2:
                # select only games with home and away teams
                if participants[0]['alignment'] == 'home':

                    # match start time
                    start_time = row['startTime'][:-1].replace('T', ' ')

                    # get match ID
                    match_id = row['id']

                    # add data to list
                    tmp_lst.append([sport_dict[sport_id], league, participants[0]['name'],
                                    participants[1]['name'], start_time, match_id])

    return tmp_lst
