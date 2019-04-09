from bs4 import BeautifulSoup
import requests
import pandas as pd 

url = "https://www.dropbox.com/s/nptpx0qb4mcycpc/readings-1464727224868.html?dl=0"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

table = soup.find_all('table')[0]
rows = table.find_all('tr')[2:]

data = {
    'Date' : [],
    'Time' : [],
    'Event' : [],
    'mg/dL' : []
}

for row in rows:
    cols = row.find_all('td')
    data['Date'].append( cols[0].get_text() )
    data['Time'].append( cols[1].get_text() )
    data['Event'].append( cols[2].get_text() )
    data['mg/dL'].append( cols[3].get_text() )

glucoseData = pd.DataFrame( data )
glucoseData.to_csv("glucose.csv")
