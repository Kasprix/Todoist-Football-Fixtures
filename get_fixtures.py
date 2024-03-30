from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse

def get_list_of_fixtures(team_id, team_name_link):
    url = f"https://www.espn.co.uk/football/team/fixtures/_/id/{team_id}/{team_name_link}"

    response = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(response).read()
    soup = BeautifulSoup(webpage, "html.parser")
    # Find all team links
    fixtures = soup.find_all('tr')

    # Iterate through each table row
    fixture_list = []
    for fixture in fixtures:
        # Extract text from each column in the current row and store in a list
        if fixture.parent.name != 'thead':
            columns = fixture.find_all('td', class_='Table__TD')
            fixture_data = [column.get_text(strip=True) for column in columns]
            
            fixture_date, home_team, away_team, fixture_time = fixture_data[0], fixture_data[1], fixture_data[3], fixture_data[4]
            fixture_list.append([fixture_date, home_team, away_team, fixture_time])
        else:
            next

    return fixture_list 

get_list_of_fixtures(364, 'liverpool')