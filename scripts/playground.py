import pandas as pd

Leagues = pd.read_csv('LeagueData.csv')

Teams = pd.read_csv('TeamDataListAttempt.csv')

# print(Leagues.sort_values(by=['Region', 'League Code'])[Leagues['Region'].str.contains('UK')])
# missing_leagues = set(Leagues['League Code'].unique()) - set(Teams['League'].unique())

# for missing_league in missing_leagues:
#     print(f"League {missing_league} is in Leagues but not in Teams.")



