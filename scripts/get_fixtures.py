from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import pandas as pd

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

    url = f"https://www.espn.co.uk/football/team/fixtures/_/id/{team_ID}/{team_name_link}"

    response = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(response).read()
    soup = BeautifulSoup(webpage, "html.parser")
    # Find all team links
    fixtures = soup.find_all('tr')
    # Remove table headers
    fixtures = [x for x in fixtures if x.parent.name != 'thead']

    # Check to see if any fixtures are upcoming
    if len(fixtures) > 0:

        num_games = get_integer_input(f"Enter the number of games you want to retrieve (Games Remaining: {len(fixtures)}): ")
        # Select lowest value of users input or max fixtures
        num_games_to_export = min(num_games, len(fixtures))

        fixture_list = []
        # Iterate through each table row
        for i in range(num_games_to_export):
            # Extract text from each column in the current row and store in a list
            fixture = fixtures[i]

            if fixture.parent.name != 'thead':
                columns = fixture.find_all('td', class_='Table__TD')
                # Remove any whitespace
                fixture_data = [column.get_text(strip=True) for column in columns]
                fixture_date, home_team, away_team, fixture_time, fixture_competition = fixture_data[0], fixture_data[1], fixture_data[3], fixture_data[4], fixture_data[5]
                fixture_list.append([fixture_date, home_team,  away_team, fixture_time, fixture_competition])
            else:
                next
    else:
        print('No upcoming fixtures')
        fixture_list = []

    return fixture_list