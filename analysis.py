import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')
'''
nba_first_year_df = pd.read_csv('nba_first_year_data.csv')
high_school_rank_df = pd.read_csv('college_player_rankings.csv')

#pure nba df from 89-21
df = pd.read_csv('nba_draft_1989_2022.csv')

#renaming the columns
nba_first_year_df = nba_first_year_df.rename(columns = {'MP':'MP_total', 'PTS':'PTS_total', 'AST': 'AST_total'
    ,'TRB':'TRB_total', 'MP.1':'MP', 'PTS.1':'PTS', 'AST.1':'AST', 'TRB.1': 'TRB'})

#joining the dataframe on players
merged_df = pd.merge(nba_first_year_df, high_school_rank_df, left_on='Player', right_on = 'PLAYER')
merged_df.to_csv('merged.csv')
'''

#simply use the merged dataset I provided
# the code above was for creating it

merged_df = pd.read_csv('merged - master.csv')

#convert pk into a float
merged_df['Pk'] = merged_df['Pk'].astype('float')

#filter for lottery picks
lottery_picks = merged_df[merged_df['Pk']<15]

# 5 star players

print("total five star players",len(high_school_rank_df[high_school_rank_df['STARS'] == 'five']))
print("drafted five star players" ,len(merged_df[merged_df['STARS'] == 'five']))

total_five_star_players = len(high_school_rank_df[high_school_rank_df['STARS'] == 'five'])
total_drafted_five_star_players = len(merged_df[merged_df['STARS'] == 'five'])
total_undrafted_five_star_players = total_five_star_players - total_drafted_five_star_players

#funnel of five start players odds to be lottery or first round picks or drafted at all

five_star_odds_lottery = len(lottery_picks[lottery_picks['STARS'] == 'five'])
print("odds of being a lottery pick", five_star_odds_lottery)

first_round_df = merged_df[merged_df['Pk'] <= 31]
five_star_odds_firstround = len(first_round_df[first_round_df['STARS'] == 'five'])
print("odds of being a first round pick", five_star_odds_firstround)

#odds of playing 30 minutes a game
playing_time_df = merged_df[merged_df['MP'] >= 30]
pt_first_round = len(playing_time_df[playing_time_df['STARS'] == 'five'])
print('odds of playing 30 minutes a game', pt_first_round)

#odds of averaging 20 points a game
scorer_df = merged_df[merged_df['PTS'] >= 20]
five_star_scorer = len(scorer_df[scorer_df['STARS'] == 'five'])
print('Odds of scoring 20 points a game', five_star_scorer)

#odds of getting drafted
print("odds of getting drafted", total_drafted_five_star_players / total_five_star_players)

#plot of 5 star players by draftpick
five_star_df = merged_df[merged_df['STARS'] == 'five']
#print(five_star_df)
picks = five_star_df.groupby('Pk').count()
picks['Player'].plot(kind='bar')


#while being a lottery pick or first rounder may seem trivial, it has a huge effect on the length of a players career
#lenght of career for each lotto picks
#for first rounders
#for second rounders
#for undrafted? look up
length_of_lotto = df[df['Pk']<=14]['G'].mean()
print('avg length of lottery picks careers:', length_of_lotto)

length_of_first_rounder = df[(df['Pk'] > 14) & (df['Pk'] < 31)]['G'].mean()
print('avg length of first round picks careers:', length_of_first_rounder)

length_of_sec_rounder = df[df['Pk'] > 30]['G'].mean()
print('avg length of second round picks careers:', length_of_sec_rounder)

print(df[(df['Pk'] < 10)]['G'].mean())
print(df[(df['Pk'] > 10) & (df['Pk'] < 20)]['G'].mean())
print(df[(df['Pk'] >= 20) & (df['Pk'] < 30)]['G'].mean())
print(df[(df['Pk'] >= 30) & (df['Pk'] < 40)]['G'].mean())
print(df[(df['Pk'] >= 40) & (df['Pk'] < 50)]['G'].mean())
print(df[(df['Pk'] >= 50)]['G'].mean())

#further breakdown of nba careers by pick
#how much shorter are second round picks careers that have a similar value (30th verus 31st)
#career length by draft pick thru the 2016 draft (average nba career lenght is 6 years)
career_length = df.iloc[:1681].groupby('Pk').agg({'G': ['sum','mean'], 'MP_total': ['sum', 'mean']})
#print(career_length)

games_played_by_pick = df.iloc[:1681].groupby('Pk').agg({'G': ['sum']})
#plt.bar(games_played_by_pick['Pk'], games_played_by_pick['sum'])
games_played_by_pick = games_played_by_pick.sort_index()
games_played_by_pick.plot(kind='bar')

avg_games_played_by_pick = df.iloc[:1681].groupby('Pk').agg({'G': ['mean']})
avg_games_played_by_pick.plot(kind='bar')
#we take picks 27:30 (late first round picks) and compare them to picks 31-34(early second round picks
#first rounder played an average of 130 games more than second rounders of a similar value and an average of 3164 minutes more
late_first_round = avg_games_played_by_pick.iloc[26:30].sum()/4
early_sec_round = avg_games_played_by_pick.iloc[30:34].sum()/4

print(late_first_round)
print(early_sec_round)
#plt.bar(games_played_by_pick.index, games_played_by_pick['sum'])
#games_played_by_pick.plot(kind='bar', x_ticks = [1,10,20,30,40,50,60])

#plt.show()

first_10_picks = merged_df[merged_df['Pk']<11]


average_rank = first_10_picks.groupby('Pk')['RK'].mean()
average_grade = first_10_picks.groupby('Pk')['GRADE'].mean()


plt.scatter(first_10_picks['Pk'], first_10_picks['RK'],  color = 'blue')
plt.scatter(average_rank.index, average_rank, color = 'red', s = 120)
plt.xlabel('NBA Draft Pick')
plt.ylabel('ESPN Ranking Pre College')
plt.xticks(first_10_picks['Pk'])
plt.yticks([0,10, 20, 30, 40, 50, 60, 70, 80])

plt.legend(['Individual Ranking', 'Average Ranking'])
#plt.show()



plt.scatter(first_10_picks['Pk'], first_10_picks['GRADE'],  color = 'blue')
plt.scatter(average_rank.index, average_grade, color = 'red', s = 120)
plt.xlabel('NBA Draft Pick')
plt.ylabel('ESPN Grade Pre College')
plt.xticks(first_10_picks['Pk'])
#plt.yticks([0,10, 20, 30, 40, 50, 60, 70, 80])

plt.legend(['Individual Grade', 'Average Grade'])



correlation = first_10_picks['Pk'].corr(first_10_picks['RK'])
print(correlation)



#look at career length by height
#height does not appear to affect career length

#merged_df['HT'] = merged_df['HT'].astype('float')

print(merged_df['HT'].unique())

heights = merged_df.groupby('HT')['G'].mean()
print(heights)
heights.plot(kind='bar')

heights.to_csv('Career_length_heigh.csv')


#career length py draft pick
career_by_pick_df = merged_df.groupby('Pk')['G'].mean()
career_by_pick_df.to_csv('career_by_pick.csv')

career_by_star_df = merged_df.groupby('STARS')[['G','Pk']]
four = career_by_star_df.get_group('four')
five = career_by_star_df.get_group('five')
four_sorted = four.groupby('Pk')['G'].mean()
five_sorted = five.groupby('Pk')['G'].mean()
five_sorted.to_csv('five_star_career_length.csv')
four_sorted.to_csv('four_star_career_length.csv')


print(four_sorted)

plt.show()






