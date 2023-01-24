import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

years = ['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']

complete_df = pd.DataFrame()

for i in range(len(years)):
        url = "http://www.espn.com/college-sports/basketball/recruiting/playerrankings/_/class/%s/order/true" % years[i]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_list = []

        # Find the table with the chart data
        tables = soup.findAll("tr")
        # Find the first row of the table
        for row in tables:
                cells = row.find_all('td')
                data = [cell.text for cell in cells]
                li = row.find('li')
                if li is not None:
                        # Retrieve the class name and append it to the data list
                        class_name = li.attrs.get('class', [])
                        data.append(' '.join(class_name))
                # Write the data to the CSV file
                # print(type(data))
                raw_list.append(data)
        # create a df
        df = pd.DataFrame(raw_list)
        # turn the first row into the columns names
        df.columns = df.iloc[0]
        # drop the first row
        df = df.iloc[1:]
        # clean the data
        df['PLAYER'] = df['PLAYER'].apply(lambda x: x.replace("Video | Scouts Report", ""))
        df['SCHOOL'] = df['SCHOOL'].apply(lambda x: x.replace('Signed', ''))
        df['SCHOOL'] = df['SCHOOL'].apply(lambda x: x.split('Committed')[0])
        df['GRADE'] = df['GRADE'].apply(lambda x: x[:2])
        df['STARS'] = df.iloc[:,-1]
        df['STARS'] = df['STARS'].astype('string')
        df['STARS'] = df['STARS'].apply(lambda x: re.split(r'[\s-]',x)[1])
        #delete the last column
        df = df.iloc[:,:-1]
        #append to complete_df
        complete_df = pd.concat([complete_df, df], ignore_index=True)

complete_df.to_csv('college_player_rankings.csv')




