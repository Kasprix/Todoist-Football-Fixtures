import os
from todoist_api_python.api import TodoistAPI
from .get_fixtures import get_list_of_fixtures
import pandas as pd
from dotenv import load_dotenv

def add_to_todoist():
    # Load environment variables from .env file
    load_dotenv()
    # Get Todoist API key from environment variable
    TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
    # Initialize Todoist API
    api = TodoistAPI(TODOIST_API_KEY)

    fixtures  = pd.DataFrame(get_list_of_fixtures(), 
                            columns=['fixture date', 'home team', 'away team', 'fixture time', 'fixture competition'])

    label = input(f"Input your preferred label for all fixtures (leave blank for no label): ")

    for index, row in fixtures.iterrows():
        try:
            task = api.add_task(
                content = f"{row['home team']} vs {row['away team']}",
                due_string= f"{row['fixture date']} at {row['fixture time']}" if row['fixture time'] != 'TBD' 
                                                                                else f"{row['fixture date']}",
                due_lang="en",
                labels= [row['fixture competition'], label] if len(label) > 0 else row['fixture competition']
            )
            print(task)
        except Exception as error:
            print(error)