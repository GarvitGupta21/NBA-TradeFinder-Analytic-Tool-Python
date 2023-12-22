import pandas as pd

def merge_data():
    contract_data = pd.read_csv('NBAcontracts.csv')
    stats_data = pd.read_csv('players.csv')

    merged_data = pd.merge(contract_data, stats_data, how='inner', left_on='Player Name', right_on='Player')

    selected_columns = ['Player', '2022/2023', 'MP', 'FGA', '3PA', 'FTA', 'FG%', '3P%', 'FT%', 'AST', 'ORB', 'DRB', 'PTS']

    final_data = merged_data[selected_columns]
    
    final_data = final_data.copy()


    final_data.loc[:, 'REB'] = final_data['ORB'] + final_data['DRB']

    final_data = final_data.drop(['ORB', 'DRB'], axis=1)
    
    final_data['Salary'] = final_data['2022/2023'].replace('[\$,]', '', regex=True).astype(float)


    #final_data = final_data.rename(columns={'2022/2023': 'Salary'})
    final_data.set_index('Player', inplace=True)
    final_data = final_data.drop(['2022/2023'], axis=1)

    final_data_filtered = final_data[(final_data['MP'] >= 7) & (final_data['FGA'] >= 4) & (final_data['3PA'] >= 2) & (final_data['FTA'] >= 3)]

    return final_data_filtered

def best_performing_player(statistic, max_salary):
    data = merge_data()

    filtered_data = data[data['Salary'] <= max_salary]

    best_player = filtered_data.loc[filtered_data[statistic].idxmax()]
    
    best_player = filtered_data.loc[filtered_data[statistic].idxmax()]
    best_player_name = best_player.name
    best_player_salary = best_player['Salary']
    best_player_stat = best_player[statistic]
    
    openFile = open("PlayerToTradeFor.txt", "w")
    openFile.write("Player to Trade For Information:\n")
    openFile.write(str(best_player.apply(lambda x: f'{x:.2f}')) + "\n")
    openFile.write("His Salary: {:.2f}\n".format(best_player_salary))
    
    openFile.write("\n")
    openFile.close()
      
    return best_player_name, best_player_salary, best_player_stat
    
