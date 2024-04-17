import os
from todoist_api_python.api import TodoistAPI
from get_fixtures import get_list_of_fixtures
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Todoist API key from environment variable
TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")

# Initialize Todoist API
api = TodoistAPI(TODOIST_API_KEY)

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
