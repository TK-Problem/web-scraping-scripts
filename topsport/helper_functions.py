def get_odds(soup, sport='Krepšinis'):
    """
    This function reads basketball data
    :param soup: bs4 element
    :param sport: str
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

    # def helper function
    def get_text(element, tag, attr):
        """
        This function text data if element is found.
        :param element: bs4 element
        :param tag: str
        :param attr: str
        :return: str
        """
        _ = element.findAll(tag, attr)
        if _:
            return _[0].text
        return ''

    # iterate over blocks
    for block in blocks:

        # get league name
        block_title = block.find('span', {'class': 'MatchListGroup__Title'})
        # replace commas with spaces
        league_name = block_title.text.replace(',', '')

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

            # get game ID
            game_id = row.findAll('a', {'class': 'Anchor Details'})
            if game_id:
                game_id = "/".join(game_id[0]['href'].split('/')[-2:])
            else:
                game_id = ''

            if sport == 'Krepšinis':
                # get AH line and odds
                ah_line = get_text(odds[0], 'span', {'class': 'OddsButton__Parameter'})
                ah_home = get_text(odds[0], 'span', {'class': 'OddsButton__Odds'})
                ah_away = get_text(odds[1], 'span', {'class': 'OddsButton__Odds'})

                # get OU odds
                ou_over = get_text(odds[2], 'span', {'class': 'OddsButton__Odds'})
                ou_under = get_text(odds[3], 'span', {'class': 'OddsButton__Odds'})

                # get OU line
                ou_line = odds[2].findAll('span', {'class': 'OddsButton__Odds'})
                if ou_line:
                    ou_line = ou_line[0].parent.parent.parent.find('span', {'class': 'OddsParameter'}).text
                else:
                    ou_line = ''

                # get ML
                ml_home = get_text(odds[4], 'span', {'class': 'OddsButton__Odds'})
                ml_away = get_text(odds[5], 'span', {'class': 'OddsButton__Odds'})

                # record data
                data.append([game_id, country_name, league_name,
                             team_names[0].text, team_names[1].text,
                             match_status,
                             pts_home, pts_away,
                             ml_home, ml_away,
                             ah_line, ah_home, ah_away,
                             ou_line, ou_over, ou_under])

            elif sport == 'Futbolas':

                # get 1x2 odds
                ml_home = get_text(odds[0], 'span', {'class': 'OddsButton__Odds'})
                ml_draw = get_text(odds[1], 'span', {'class': 'OddsButton__Odds'})
                ml_away = get_text(odds[2], 'span', {'class': 'OddsButton__Odds'})

                # get OU line
                ou_line = odds[3].findAll('span', {'class': 'OddsButton__Odds'})
                if ou_line:
                    ou_line = ou_line[0].parent.parent.parent.find('span', {'class': 'OddsParameter'}).text
                else:
                    ou_line = ''

                # get OU odds
                ou_over = get_text(odds[3], 'span', {'class': 'OddsButton__Odds'})
                ou_under = get_text(odds[4], 'span', {'class': 'OddsButton__Odds'})

                # record data
                data.append([game_id, country_name, league_name,
                             team_names[0].text, team_names[1].text,
                             match_status,
                             pts_home, pts_away,
                             ml_home, ml_draw, ml_away,
                             ou_line, ou_over, ou_under])

            elif sport == 'Ledo ritulys':

                # get 1x2 odds
                ml_home = get_text(odds[0], 'span', {'class': 'OddsButton__Odds'})
                ml_draw = get_text(odds[1], 'span', {'class': 'OddsButton__Odds'})
                ml_away = get_text(odds[2], 'span', {'class': 'OddsButton__Odds'})

                # get AH line
                ah_line = get_text(odds[3], 'span', {'class': 'OddsButton__Parameter'})
                ah_home = get_text(odds[3], 'span', {'class': 'OddsButton__Odds'})
                ah_away = get_text(odds[4], 'span', {'class': 'OddsButton__Odds'})

                # get OU odds
                ou_over = get_text(odds[5], 'span', {'class': 'OddsButton__Odds'})
                ou_under = get_text(odds[6], 'span', {'class': 'OddsButton__Odds'})

                # get OU line
                ou_line = odds[5].findAll('span', {'class': 'OddsButton__Odds'})
                if ou_line:
                    ou_line = ou_line[0].parent.parent.parent.find('span', {'class': 'OddsParameter'}).text
                else:
                    ou_line = ''

                data.append([game_id, country_name, league_name,
                             team_names[0].text, team_names[1].text,
                             match_status,
                             pts_home, pts_away,
                             ml_home, ml_draw, ml_away,
                             ah_line, ah_home, ah_away,
                             ou_line, ou_over, ou_under])

    return data
