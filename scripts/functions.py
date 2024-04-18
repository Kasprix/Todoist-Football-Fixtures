from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from tqdm import tqdm  
import random  
import time 

def get_list_of_leagues():
    """
    Retrieves a list of football leagues from ESPN website.

    Returns:
        pd.DataFrame: DataFrame containing league data (League, League Code, Region),
                      sorted by region and league code.
    """
    url = "https://www.espn.co.uk/football/competitions"
    response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(response).read()
    soup = BeautifulSoup(webpage, "html.parser")

    # Find all team links
    team_links = soup.find_all('a', class_='AnchorLink', href=lambda x: x and '/football/teams/_/league/' in x)

    exclusion_set = {'Internationals', 'Top Competitions'}
    league_data = []

    for team_link in team_links:
        # Check if the league name is not in the exclusion set
        previous_h3 = team_link.find_previous('h3')
        if previous_h3.getText() not in exclusion_set:
            team_id = urlparse(team_link['href']).path.split('/')[-1]
            league_name_user = team_link.find_previous('h2').text
            league_data.append([league_name_user, team_id, previous_h3.getText()])

    # Create DataFrame and save it to a CSV file
    league_data_df = pd.DataFrame(league_data, columns=['League', 'League Code', 'Region']).sort_values(by=['Region', 'League Code'])
    league_data_df.to_csv(r'data\LeagueData.csv', index=False)

    return league_data_df

def get_teams_from_league(leagues='ENG.1'):
    """
    Retrieves teams from football leagues specified by league codes.

    Args:
        leagues (str or list): League codes or a single league code.

    Returns:
        pd.DataFrame: DataFrame containing team data (Team Name, Team ID, Team Name Link, League Code),
                      sorted by league code and team name.
    """
    teams_dic = {}
    failed_leagues = []
    league_data = []

    # Loop through each league code
    for league in tqdm(leagues):
        print(f"Scraping league: {league}")

        # Construct URL for the league
        url = f"https://www.espn.co.uk/football/teams/_/league/{league}"
        response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(response).read()
        soup = BeautifulSoup(webpage, "html.parser")

        # Find all team links
        team_links = soup.find_all('a', class_='AnchorLink', href=lambda x: x and '/football/team/fixtures/_/id/' in x)

        counter = 0
        for team_link in team_links:
            # Extract team data from the team link
            team_id = team_link['href'].split('/football/team/fixtures/_/id/')[1].split('/')[0]
            team_name_link = team_link['href'].split('/football/team/fixtures/_/id/')[1].split('/')[1]
            team_name_user = team_link.find_previous('h2').text
            teams_dic[team_name_user] = [team_id, team_name_link, league]

            league_data.append([team_name_user, team_id, team_name_link, league])
            counter += 1

        print(f"Scraped {counter} teams from {league}")

        # Check if 'ENG.1' exists in any value of teams_dic
        if any(league in value for value in teams_dic.values()):
            continue
        else:
            failed_leagues.append(league)
        
        # Add a random delay between 1 and 3 seconds to avoid overdoing the same requests
        time.sleep(random.uniform(1, 3))

    print(f"Failed leagues: {failed_leagues}")

    # Create DataFrame
    team_data_df = pd.DataFrame(league_data, columns=['Team Name', 'Team ID', 'Team Name Link', 'League Code']).sort_values(by=['League Code', 'Team Name'])

    return team_data_df

def export_all_to_CSV():
    """
    Retrieves leagues and teams, merges them, and exports the data to a CSV file.

    The CSV file contains league and team data merged on the league code.
    """
    # Retrieve league data
    leagues = get_list_of_leagues()

    # Retrieve team data for the leagues
    teams = get_teams_from_league(leagues['League Code'])

    # Merge leagues and teams data
    merged_df = pd.merge(teams, leagues, on='League Code', how='inner')

    # Export merged data to CSV
    merged_df.to_csv(r'data\LeagueAndTeamData.csv', index=False)
    merged_df.info()
