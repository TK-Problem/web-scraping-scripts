def process_data(soup, sport='Basketball'):
    """
    This function returns processed data beased on sport
    :param soup:
    :param sport:
    :return:
    """
    # get all competitions
    comp = soup.findAll('div', {'class': 'ovm-Competition ovm-Competition-open'})

    # create empty list for storing data
    data_lst = []

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
            game_status = event.findAll('div', {'class': 'ovm-FixtureDetailsTwoWay_Period ovm-PeriodInfo'})
            if game_status:
                game_status = game_status[0].text
            else:
                game_status = ''

            # game time
            game_time = event.findAll('div', {'class': 'ovm-FixtureDetailsTwoWay_Timer ovm-InPlayTimer'})
            if game_time:
                game_time = game_time[0].text
            else:
                game_time = ''

            # scores
            pts_home = event.find('div', {'class': 'ovm-StandardScores_TeamOne'}).text
            pts_away = event.find('div', {'class': 'ovm-StandardScores_TeamOne'}).text

            # get all markets
            markets = event.findAll('div', {'class': 'ovm-Market'})

            if sport in ['Basketball']:

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

                data_lst.append([league, home_name, away_name,
                                 game_status, game_time,
                                 pts_home, pts_away,
                                 ah_line, ah_home, ah_away,
                                 ou_line, ou_over, ou_under,
                                 ml_home, ml_away])

    return data_lst
