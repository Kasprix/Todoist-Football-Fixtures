import os
from todoist_api_python.api import TodoistAPI
import pandas as pd
from dotenv import load_dotenv
from .get_fixtures import get_list_of_fixtures

def add_to_todoist():
    """
    Retrieves upcoming fixtures and adds them as tasks to Todoist.

    Retrieves fixture data using the get_list_of_fixtures function, prompts the user
    to input a label for all fixtures, and adds each fixture as a task to Todoist.
    The task content includes the home team and away team names, and the due date
    is set based on the fixture date and time. Optionally, a label specified by the
    user is added to each task.

    Raises:
        Exception: If there's an error adding a task to Todoist.
    """
    
    # Load environment variables from .env file
    load_dotenv()
    # Get Todoist API key from environment variable
    todoist_api_key = os.getenv("TODOIST_API_KEY")
    # Initialize Todoist API
    api = TodoistAPI(todoist_api_key)

    # Get fixtures data
    fixtures = pd.DataFrame(get_list_of_fixtures(), 
                            columns=['fixture date', 'home team', 'away team', 'fixture time', 'fixture competition'])

    # Input label
    label = input("Input your preferred label for all fixtures (leave blank for no label): ")

    # Iterate through fixtures
    for _, row in fixtures.iterrows():
        try:
            # Construct task content and due string
            task_content = f"{row['home team']} vs {row['away team']}"
            due_string = f"{row['fixture date']} at {row['fixture time']}" if row['fixture time'] != 'TBD' else f"{row['fixture date']}"

            # Construct labels list
            task_labels = [row['fixture competition']]
            if label:
                task_labels.append(label)

            # Add task to Todoist
            task = api.add_task(
                content=task_content,
                due_string=due_string,
                due_lang="en",
                labels=task_labels
            )
            print(task)
        except Exception as error:
            print(error)
