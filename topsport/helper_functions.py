def get_basketball_odds(soup):
    """
    This function reads basketball data
    :param soup:
    :return: list
    """
    # find All leagues
    blocks = soup.findAll('div', {'class': 'MatchListGroup MatchList__Group'})
    # find countries
    countries = soup.findAll('span', {'class': 'OM-Slider__ItemIcon'})
    countries = {_.span['style'].split('/')[-1][:-7]: _.parent.find('div', {'class': 'OM-Slider__ItemText'}).text for _
                 in countries}

    # create empty list to store data
    data = list()

    # iterate over blocks
    for block in blocks:

        # get league name
        block_title = block.find('span', {'class': 'MatchListGroup__Title'})
        league_name = block_title.text

        # get country flag code
        country_name = block_title.parent.span.span['style'].split('/')[-1][:-7]
        country_name = countries[country_name]

        # find all events for specific league
        rows = block.findAll('div', {'class': 'MatchListGroup__Content'})

        # iterate over rows/events
        for row in rows:

            # get current match time
            match_status = row.find('span', {'class': 'MatchTime MatchTime--Progress EventItem__Info'}).text

            # get team names
            team_names = row.findAll('span', {'class': 'Details__ParticipantName'})

            # get scores for home and away teams
            pts_home = row.find('span', {'class': 'Score__Part Score__Part--Home'}).text
            pts_away = row.find('span', {'class': 'Score__Part Score__Part--Away'}).text

            # get odds content
            odds = row.findAll('button', {'data-ubt-page': 'liveSports'})

            # get AH line
            ah_line = odds[0].findAll('span', {'class': 'OddsButton__Parameter'})
            if ah_line:
                ah_line = ah_line[0].text
                ah_home = odds[0].find('span', {'class': 'OddsButton__Odds'}).text
                ah_away = odds[1].find('span', {'class': 'OddsButton__Odds'}).text
            else:
                ah_line, ah_home, ah_away = '', '', ''

            # get OU line and odds
            ou_line = odds[2].findAll('span', {'class': 'OddsButton__Odds'})
            if ou_line:
                ou_over = ou_line[0].text
                ou_under = odds[3].find('span', {'class': 'OddsButton__Odds'}).text
                ou_line = ou_line[0].parent.parent.parent.find('span', {'class': 'OddsParameter'}).text
            else:
                ou_over, ou_under, ou_line = '', '', ''

            # get ML
            ml = odds[4].findAll('span', {'class': 'OddsButton__Odds'})
            if ml:
                ml_home = ml[0].text
                ml_away = odds[5].findAll('span', {'class': 'OddsButton__Odds'})
                if ml_away:
                    ml_away = ml_away[0].text
                else:
                    ml_away = ''
            else:
                ml_home = ''
                ml_away = ''

            data.append([country_name, league_name,
                         team_names[0].text, team_names[1].text,
                         match_status,
                         pts_home, pts_away,
                         ml_home, ml_away,
                         ah_line, ah_home, ah_away,
                         ou_line, ou_over, ou_under])

    return data
