import requests
import bs4
import re
import time

response = requests.get('http://calcio-seriea.net/risultati/2014');
soup = bs4.BeautifulSoup(response.text, "html.parser");
# print response
# print soup
tables = soup.find_all('table');
fixtures = tables[8];

# print tables
rows = fixtures.find_all('tr');

dates = rows[0].find_all('a') + rows[1].find_all('a');

for date in dates:
	dateURL = "http://calcio-seriea.net" + date['href'];
	print dateURL;
	






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
