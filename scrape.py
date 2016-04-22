import requests
import bs4
import re
import time

#Page for a season:
response = requests.get('http://calcio-seriea.net/risultati/2014');
soup = bs4.BeautifulSoup(response.text, "html.parser");
tables = soup.find_all('table');
#Table for each fixture:
fixtures = tables[8];
rows = fixtures.find_all('tr');
dates = rows[0].find_all('a') + rows[1].find_all('a');

#For each fixture:
for date in dates:
	#Get fixture number:
	fixture = date.text.strip();
	dateURL = "http://calcio-seriea.net" + date['href'];
	#Page for each date:
	response = requests.get(dateURL);
	soup = bs4.BeautifulSoup(response.text, "html.parser");

	tables = soup.find_all('table');
	results = tables[11];
	games = results.find_all('tr');

	#For each game:
	for game in games:
		objects = game.find_all('a');
		if len(objects) == 0: continue;
		homeTeam = objects[0].text.strip();
		awayTeam = objects[1].text.strip();
		gameResult = objects[2].text.strip();
		gameURL = "http://calcio-seriea.net" + objects[2]['href'];

		
		#Page for each game:
		response = requests.get(gameURL);
		soup = bs4.BeautifulSoup(response.text, "html.parser");
		tables = soup.find_all('table');

		gameStats = tables[8];
		rows = gameStats.find_all('tr');

		gameStats.find_all('tr')[14].find_all('td')[0]










# linklist=[]
# for row in rows:

#     objlist = row.find_all('a')
#     if len(objlist)>0:
#         obj=objlist[0]
#         if obj.has_attr('href'):
#             linklist.append(obj['href'])

# urllist=[]
# for part in linklist:
#     url="http://www.basketball-reference.com"+part
#     urllist.append(url)

# for url in urllist:
#     processpage(url)
#     time.sleep(1)
