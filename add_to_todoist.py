from todoist_api_python.api import TodoistAPI
from get_fixtures import get_list_of_fixtures
import pandas as pd

api = TodoistAPI("f7c2afd2b24f7f01ebf72b6cb269d980cb01c3da")

fixtures = league_data_df = pd.DataFrame(get_list_of_fixtures(364, 'liverpool'), 
                                         columns=['fixture date', 'home team', 'away team', 'fixture time'])

for index, row in fixtures.head(5).iterrows():
    try:
        task = api.add_task(
            content = f"{row['home team']} vs {row['away team']}",
            due_string= f"{row['fixture date']} at {row['fixture time'])}",
            due_lang="en",
            labels=['Football Games']
        )
        print(task)
    except Exception as error:
        print(error)