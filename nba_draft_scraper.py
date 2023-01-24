#this scrapes nba draft data
import requests
from bs4 import BeautifulSoup
import pandas as pd

years = list(range(1989,2023))

complete_df = pd.DataFrame(columns=['Pk', 'Tm', 'Player', 'College', 'Yrs', 'G', 'MP', 'PTS', 'TRB', 'AST', 'FG%', '3P%', 'FT%', 'MP' , 'PTS', 'TRB', 'AST'])
for year in range(len(years)):
    response = requests.get('https://www.basketball-reference.com/draft/NBA_%s.html' % years[year])
    soup = BeautifulSoup(response.content, 'html.parser')
    #soup = BeautifulSoup(response.content, 'lxml')

    raw_list = []

    table = soup.find('table')

    # Collecting Ddata
    for row in table.tbody.find_all('tr'):
        # Find all data for each column
        columns = row.find_all('td')
        data = [cell.text for cell in columns]
        raw_list.append(data)
    df = pd.DataFrame(raw_list)
    df = df.iloc[:, :-4]
    df.columns = ['Pk', 'Tm', 'Player', 'College', 'Yrs', 'G', 'MP', 'PTS', 'TRB', 'AST', 'FG%', '3P%', 'FT%', 'MP',
                  'PTS', 'TRB', 'AST']
    complete_df = pd.concat([complete_df, df], ignore_index=True)
complete_df.dropna(thresh = 2)
complete_df.to_csv('complete_nba_first_year_data.csv')



