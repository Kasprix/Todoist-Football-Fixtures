from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse
import time, random

def get_list_of_leagues():
    url = f"https://www.espn.co.uk/football/competitions"
    response = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(response).read()
    soup = BeautifulSoup(webpage, "html.parser")

    # Find all team links
    team_links = soup.find_all('a', class_='AnchorLink', href=lambda x: x and '/football/teams/_/league/' in x)

    # league_dict = {}
    # for team_link in team_links:
    #     previous_h3 = team_link.find_previous('h3')
    #     if previous_h3.getText() not in ('Internationals', 'Top Competitions'):
    #         team_id = team_link['href'].split('/football/teams/_/league/')[1]
    #         # print(team_link['href'].split('/football/teams/_/league/')[1])
    #         league_name_user = team_link.find_previous('h2').text
    #         # print(team_link.find_previous('h2').text)
    #         league_dict[league_name_user] = [team_id, previous_h3.getText()]
    #         # print(previous_h3.getText(), '|', team_id, '|', league_name_user)

    league_data = []
    exclusion_set = {'Internationals', 'Top Competitions'}


    for team_link in team_links:
        previous_h3 = team_link.find_previous('h3')
        if previous_h3.getText() not in exclusion_set:
            team_id = urlparse(team_link['href']).path.split('/')[-1]
            league_name_user = team_link.find_previous('h2').text
            league_data.append([league_name_user, team_id, previous_h3.getText()])

    # Convert the list to a DataFrame
    league_data_df = pd.DataFrame(league_data, columns=['League', 'League Code', 'Region']).sort_values(by=['Region', 'League Code'])

    # # Convert the dictionary to a DataFrame
    # league_data_df = pd.DataFrame(list(league_dict.items()), columns=['League', 'League Info'])

    # # Split the 'League Info' column into 'League Code' and 'Region'
    # league_data_df[['League Code', 'Region']] = pd.DataFrame(league_data_df['League Info'].tolist(), index=league_data_df.index)
    # # print(league_data_df)

    # # Drop the original 'League Info' column
    # league_data_df = league_data_df.drop(columns=['League Info'])

    league_data_df.to_csv(r'data\LeagueData.csv', index=False)

    return league_data_df

def get_teams_from_league(leagues = 'ENG.1') :
    teams_dic = {}
    failed_leagues = []
    league_data = []


    for league in tqdm(leagues):
        print(f"Scraping league: {league}")

        url = f"https://www.espn.co.uk/football/teams/_/league/{league}"
        response = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

        webpage = urlopen(response).read()
        soup = BeautifulSoup(webpage, "html.parser")

        # Find all team links
        team_links = soup.find_all('a', class_='AnchorLink', href=lambda x: x and '/football/team/fixtures/_/id/' in x)

        counter = 0
        for team_link in team_links:
            team_id = team_link['href'].split('/football/team/fixtures/_/id/')[1].split('/')[0]
            # print(team_id)
            team_name_link = team_link['href'].split('/football/team/fixtures/_/id/')[1].split('/')[1]
            #print(team_name_link)
            team_name_user = team_link.find_previous('h2').text
            #print(team_name_user)
            teams_dic[team_name_user] = [team_id, team_name_link, league]

            league_data.append([team_name_user, team_id, team_name_link, league])
            counter += 1

        print(f"Scraped {counter} teams from {league}")

        # Check if 'ENG.1' exists in any value of teams_dic
        if any(league in value for value in teams_dic.values()):
            continue
        else:
            failed_leagues.append(league)
        # Add a random delay between 1 and 3 seconds
            
        # to avoid overdoing the same requests
        time.sleep(random.uniform(1, 3))

    print(f"Failed leagues: {failed_leagues}")

    # Convert the dictionary to a DataFrame
    team_data_df = pd.DataFrame(league_data, columns=['Team Name', 'Team ID', 'Team Name Link', 'League Code']).sort_values(by=['League Code', 'Team Name'])

    return team_data_df

def export_all_to_CSV() :
    leagues = get_list_of_leagues()

    teams = get_teams_from_league(leagues['League Code'])

    merged_df = pd.merge(teams, leagues, on='League Code', how='inner')

    merged_df.to_csv(r'data\LeagueAndTeamData.csv', index=False)

    merged_df.info()


#TODO: Create a search function for each team that takes the normal name and gets the team ID and the team name link
def get_list_of_fixtures():

    team_table = pd.read_csv(r'data\LeagueAndTeamData.csv')
    
    # Function to get an integer input from the user
    def get_integer_input(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Please enter a valid integer.")

    
    # Function to confirm the input
    def confirm_input(value):
        confirmation = input(f"Confirm input: {value} (yes/no)? ").lower()
        return confirmation == "yes"
    
    
    # Prompt user for integer input
    while True:
        team_ID = get_integer_input("Enter the ID you want to search for: ")
        
        try:
            team_name_link =  team_table.loc[team_table['Team ID'] == team_ID, 'Team Name Link'].iloc[0]
            print(f"The team name of {team_ID} is {team_name_link}.")
        except IndexError:
            print("ID not found in table.")
            continue
        
        
        if confirm_input(team_ID):
            break
        else:
            print("Redoing the search...")

get_list_of_fixtures()