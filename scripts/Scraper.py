import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re


url = "https://www.espn.co.uk/football/teams/_/league/ENG.1"
response = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(response).read()
soup = BeautifulSoup(webpage, "html.parser")

# Find all team links
team_links = soup.find_all('a', class_='AnchorLink', href=lambda x: x and '/football/team/fixtures/_/id/' in x)

teams_dic = {}

for team_link in team_links:
    team_id = team_link['href'].split('/football/team/fixtures/_/id/')[1].split('/')[0]
    # print(team_id)
    team_name_link = team_link['href'].split('/football/team/fixtures/_/id/')[1].split('/')[1]
    #print(team_name_link)
    team_name_user = team_link.find_previous('h2').text
    #print(team_name_user)
    teams_dic[team_name_user] = [team_id, team_name_link]


# # Print the team names and IDs
# for team_link in team_links:
#     team_name_tag = team_link.find('h2', class_='h5')
#     print(team_name_tag)

# for team_link in team_links:
#     # team_name = team_link.find_children()
#     team_name = team_link.find_next_sibling("h2").text

#     print(team_name)
#     team_id = team_link['href'].split('/football/team/fixtures/_/id/')[1].split('/')[0]

#     print(team_id)

# for team_link in team_links:
#     team_name = team_link.find('h2').text
#     team_id = team_link['href'].split('/id/')[1].split('/')[0]
    
#     print(f"Team: {team_name}, ID: {team_id}")
    
#     # Now you can proceed to scrape the fixtures for each team using their IDs
#     fixtures_url = f"https://www.espn.co.uk/football/team/fixtures/_/id/{team_id}/{team_name.lower().replace(' ', '-')}"
#     # Use the fixtures_url to fetch and process the fixture data
#     # ...

