import pandas as pd
import teamStatsLib as tsl
import playerFinderLib as pfl

print ("Wlecome to Bucket Finder!")
print()
while True:
    season = input("Please enter an NBA season year: ")

    try:
        season = int(season)
        if 2014 <= season <= 2022:
            break
        else:
            print("Error: Season must be an integer between 2014 and 2022.")
    except ValueError:
        print("Error: Please enter a valid NBA Season.")
        

team = input("Please enter a team abbreviation: ")

print(f"Your are the manager of {season} {team} Franchise: ")

most_negative_stat, most_negative_value = tsl.final_output(season, team)
print()
print(f"Your Team's Worst Statistic is: '{most_negative_stat}' and it is {most_negative_value} percent less than the league's average.")
print()
salaryCap = float(input("Please enter your remaining NBA salary CAP: "))
tradeName,tradeSalary, tradeStat = pfl.best_performing_player(most_negative_stat, salaryCap)
print()
print(f'The Player you should trade for is: {tradeName}')
print(f'His Salary is : {tradeSalary}')
print(f'His {most_negative_stat} average is: {tradeStat} and is the best player for your team in your budget.')
print()
print('Complete Stats for your player can be found in the PlayerToTradeFor.txt file.')


""" TEAM ABBREVIATIONS:
ATL	Atlanta Hawks
BOS	Boston Celtics
BKN	Brooklyn Nets
CHA	Charlotte Hornets
CHI	Chicago Bulls
CLE	Cleveland Cavaliers
DAL	Dallas Mavericks
DEN	Denver Nuggets
DET	Detroit Pistons
GSW Golden State Warriors
HOU	Houston Rockets
IND	Indiana Pacers
LAC	Los Angeles Clippers
LAL	Los Angeles Lakers
MEM	Memphis Grizzlies
MIA	Miami Heat
MIL	Milwaukee Bucks
MIN	Minnesota Timberwolves
NOP New Orleans Pelicans
NYK New York Knicks
OKC	Oklahoma City Thunder
ORL	Orlando Magic
PHI	Philadelphia 76ers
PHX	Phoenix Suns
POR	Portland Trail Blazers
SAC	Sacramento Kings
SAS San Antonio Spurs
TOR	Toronto Raptors
UTA Utah Jazz
WAS	Washington Wizards """



    
    



