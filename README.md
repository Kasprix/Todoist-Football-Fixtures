# Football Fixtures to Todoist

This Python project automates the process of adding upcoming football fixtures to Todoist task lists using the Todoist API. It scrapes fixture data from the ESPN website, including leagues, teams, and upcoming matches, and seamlessly integrates it into your Todoist account for easy tracking.

## Features

- Utilizes the Todoist API to add upcoming football fixtures to your Todoist task list.
- Scrapes football fixture data from ESPN website, including leagues, teams, and match schedules.
- Provides functionality to fetch a list of leagues and teams, as well as upcoming fixtures for specific teams.
- Saves the scraped data into CSV files for further analysis or usage.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/football-fixtures-to-todoist.git
    ```

2. Navigate to the project directory:

    ```bash
    cd football-fixtures-to-todoist
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have Python installed on your system.
2. Set up a Todoist API key and replace `"YOUR_API_KEY"` in `add_to_todoist.py` with your actual API key.
3. Run the `add_to_todoist.py` script to add upcoming fixtures to your Todoist task list:

    ```bash
    python add_to_todoist.py
    ```

4. The script will automatically add upcoming fixtures to your Todoist task list.

## Notes

- This project is intended for educational purposes and should be used responsibly and in compliance with the terms of use of the ESPN website and Todoist API.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.
