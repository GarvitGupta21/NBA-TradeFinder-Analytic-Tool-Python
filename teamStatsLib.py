import pandas as pd
import matplotlib.pyplot as plt


# Function to calculate average stats for each team for the selected season
def calculate_team_stats(selected_season):
    
    file_path = 'games.csv'  
    df = pd.read_csv(file_path)

    teams_path = 'teams.csv'  
    teams_df = pd.read_csv(teams_path)

    team_id_mapping = dict(zip(teams_df['TEAM_ID'], teams_df['ABBREVIATION']))
    
    filtered_df = df[df['SEASON'] == selected_season]

    team_stats_home = filtered_df.groupby('TEAM_ID_home').agg({
        'PTS_home': 'mean',
        'FG_PCT_home': 'mean',
        'FT_PCT_home': 'mean',
        'FG3_PCT_home': 'mean',
        'AST_home': 'mean',
        'REB_home': 'mean',
    }).reset_index()

    team_stats_away = filtered_df.groupby('TEAM_ID_away').agg({
        'PTS_away': 'mean',
        'FG_PCT_away': 'mean',
        'FT_PCT_away': 'mean',
        'FG3_PCT_away': 'mean',
        'AST_away': 'mean',
        'REB_away': 'mean',
    }).reset_index()

    team_stats = pd.merge(team_stats_home, team_stats_away, how='outer', left_on='TEAM_ID_home', right_on='TEAM_ID_away', suffixes=('_home', '_away'))
    
    team_stats = team_stats.fillna(0)

    for col in ['PTS', 'FG_PCT', 'FT_PCT', 'FG3_PCT', 'AST', 'REB']:
        team_stats[col] = (team_stats[f'{col}_home'] + team_stats[f'{col}_away']) / 2

    team_stats = team_stats[['TEAM_ID_home', 'PTS', 'FG_PCT', 'FT_PCT', 'FG3_PCT', 'AST', 'REB']]
    team_stats = team_stats.rename(columns={'TEAM_ID_home': 'TEAM_ID'})
    
    team_stats['TEAM_ABBREVIATION'] = team_stats['TEAM_ID'].map(team_id_mapping)
    
    team_stats.set_index('TEAM_ABBREVIATION', inplace=True)
    
    return team_stats

#Function to caclulate league's average stats for each team 
def calculate_overall_averages(team_stats):
    overall_averages = team_stats[['PTS', 'FG_PCT', 'FT_PCT', 'FG3_PCT', 'AST', 'REB']].mean().to_frame().T
    overall_averages['TEAM_ABBREVIATION'] = 'LEAGUE'
    overall_averages.set_index('TEAM_ABBREVIATION', inplace=True)
    return overall_averages

# Function to select a team to compare to
def select_team_for_comparison(team_stats, team_abbreviation):
        selected_team_stats = team_stats.loc[team_abbreviation]
        return selected_team_stats
    
# Function to compare team statistics to league averages
def compare_team_to_league(selected_team_stats, overall_averages, season):
    
    differences = selected_team_stats - overall_averages
    differences = differences.drop('TEAM_ID', axis=1, errors='ignore')
    percent_change = (differences / overall_averages) * 100
    
    # Plot 
    ax = percent_change.plot(kind='bar', title=f'Team Stats vs. League Averages in the {season} season', figsize=(10, 6))
    ax.set_ylabel('Percent Difference between Team average and League Average')
    ax.set_xlabel('Statistic')
    
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return percent_change


# Function to find the most negative statistic in the differences DataFrame
def find_most_negative_statistic(perentChange):
    most_negative_stat = perentChange.idxmin(axis=1)
    most_negative_value = perentChange.min(axis=1)
 
    if most_negative_stat.str.contains('AST').any():
        most_negative_stat = 'AST'
    elif most_negative_stat.str.contains('FG3_PCT').any():
        most_negative_stat = '3P%'
    elif most_negative_stat.str.contains('FG_PCT').any():
        most_negative_stat = 'FG%'
    elif most_negative_stat.str.contains('FT_PCT').any():
        most_negative_stat = 'FT%'
    elif most_negative_stat.str.contains('REB').any():
        most_negative_stat = 'REB'
    elif most_negative_stat.str.contains('PTS').any():
        most_negative_stat = 'PTS'
    
    most_negative_value = most_negative_value.astype(str).str.extract(r'([-+]?\d*\.\d+|\d+)').astype(float).values[0]
       
    return most_negative_stat, most_negative_value 


def final_output(season, team_abbreviation):
    team_stats = calculate_team_stats(season)
    overall_averages = calculate_overall_averages(team_stats)
    selected_team_stats = select_team_for_comparison(team_stats, team_abbreviation)
    percentChange = compare_team_to_league(selected_team_stats, overall_averages, season)
    most_negative_stat, most_negative_value = find_most_negative_statistic(percentChange)
    #print(f"Your Team's Worst Statistic is: '{most_negative_stat}' with a {most_negative_value} percent less than the league's average.")
    return most_negative_stat, most_negative_value


###main method###

# Example: Calculate average stats for each team for the selected season
""" selected_season = 2022  # Replace with the season of interest
team_stats = calculate_team_stats(selected_season)

# Display the calculated team statistics
print("\nCombined Team Statistics for Home and Away Teams:")
print(team_stats)

# Calculate overall averages for each statistic for the entire year
overall_averages = calculate_overall_averages(team_stats)
print("\nOverall Averages for the Entire League:")
print(overall_averages)

selected_team_stats = select_team_for_comparison(team_stats, 'LAL')

# Compare the selected team's statistics to the league averages
percentChange = compare_team_to_league(selected_team_stats, overall_averages)
print("\nComparison of Team Statistics to League Averages:")
print(percentChange)

# Example usage:
most_negative_stat, most_negative_value = find_most_negative_statistic(percentChange)

# Display the result
print(f"The most negative statistic is '{most_negative_stat}' with a value of {most_negative_value}." )"""

#x,y = final_output(2022, 'LAL')


#print (x,y)



