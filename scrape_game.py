import requests
import bs4
import re
import time

urlFile = open("gameUrl.txt",'r');
results = open("results.csv",'w');

while(True):
	gameURL = urlFile.readline();
	if len(gameURL) == 0: break;

	#gameURL = "http://calcio-seriea.net/tabellini/2007/21804/";

	#Page for each game:
	response = requests.get(gameURL);
	soup = bs4.BeautifulSoup(response.text, "html.parser");
	tables = soup.find_all('table');

	league_plus_season = tables[6].find_all('tr')[0].find_all('td')[0].text.strip();
	meta_league = league_plus_season[0:7];
	meta_season = league_plus_season[8:];

	match_info_rows = tables[7].find_all('tr');
	meta_fixture = match_info_rows[1].text.strip();
	meta_date = match_info_rows[2].text.strip();
	meta_stadium = match_info_rows[3].text.strip();
	meta_ref = ' '.join(match_info_rows[4].text.strip()[8:].strip().split());

	gameStats_rows = tables[8].find_all('tr');

	team_plus_score = gameStats_rows[0].text.strip().split();

	meta_team1 = team_plus_score[0];
	meta_goals1 = team_plus_score[1];
	meta_goals2 = team_plus_score[2];
	meta_team2 = team_plus_score[3];

	r_titolari = -1;
	r_disposizione = -1;
	r_allenatore = -1;

	for i in range(len(gameStats_rows)):
		row = gameStats_rows[i];
		if "TITOLARI" in row.text:
			r_titolari = i;
		if "DISPOSIZIONE" in row.text:
			r_disposizione = i;
		if "ALLENATORE" in row.text:
			r_allenatore = i;

	print r_titolari,r_disposizione,r_allenatore
	
	meta_goalscorer1 = [];
	meta_goalscorer2 = [];
	meta_goaltime1 = [];
	meta_goaltime2 = [];

	#goals:
	for i in range(1, r_titolari):
		fields = gameStats_rows[i].find_all('td');
		if len(fields) < 2: continue;
		#team 1 goal:
		if len(fields[0].text.strip()) != 0:
			meta_goalscorer1.append(fields[0].text.strip());
			meta_goaltime1.append(fields[1].text.strip());
		#team 2 goal:
		else:
			meta_goalscorer2.append(fields[5].text.strip());
			meta_goaltime2.append(fields[4].text.strip());

	meta_player1 = [];
	meta_player2 = [];
	meta_yellow1 = [];
	meta_yellow2 = [];
	meta_red1 = [];
	meta_red2 = [];
	meta_sub1 = [];
	meta_sub2 = [];

	#starting11:
	for i in range(r_titolari + 1, r_allenatore):

		if i == r_disposizione: continue;

		fields = gameStats_rows[i].find_all('td');

		#players:
		meta_player1.append(fields[1].text.strip());
		meta_player2.append(fields[8].text.strip())

		#sub:
		if len(fields[3].text.strip()) != 0:
			meta_sub1.append(fields[3].text.strip());
		else:
			meta_sub1.append("");	
		if len(fields[6].text.strip()) != 0:
			meta_sub2.append(fields[6].text.strip());
		else:
			meta_sub2.append("");	

		#cards:
		if len(fields[0].find_all('img')) == 0:
			meta_yellow1.append("");
			meta_red1.append("");
		else:
			if 'ammonito' in fields[0].img['alt']:
				meta_yellow1.append("true");
			else:
				meta_yellow1.append("");

			if 'espulso' in fields[0].img['alt']:
				meta_red1.append("true");
			else:
				meta_red1.append("");

		if len(fields[9].find_all('img')) == 0:
			meta_yellow2.append("");
			meta_red2.append("");
		else:
			if 'ammonito' in fields[9].img['alt']:
				meta_yellow2.append("true");
			else:
				meta_yellow2.append("");

			if 'espulso' in fields[9].img['alt']:
				meta_red2.append("true");
			else:
				meta_red2.append("");


	meta_coach1 = "";
	meta_coach2 = "";
	if r_allenatore != -1:
		fields = gameStats_rows[r_allenatore + 1].find_all('td');
		meta_coach1 = fields[0].text.strip();
		meta_coach2 = fields[3].text.strip();

	results.write(meta_league +","+ meta_season +","+ meta_fixture +","+ meta_date +","+ meta_stadium +","+ meta_ref +","+ meta_team1 +","+ meta_goals1 +","+ meta_team2 +","+ meta_goals2 + "," + meta_coach1 + "," + meta_coach2);
	results.write(";".join(meta_goalscorer1) +","+ ";".join(meta_goaltime1) +","+ ";".join(meta_goalscorer2) +","+ ";".join(meta_goaltime2)+ "," );
	for i in range(11):
		results.write(meta_player1[i].encode('utf-8'));
		results.write(";");
		if meta_yellow1[i] == "true":
			results.write("yellow");
		results.write(";");
		if meta_red1[i] == "true":
			results.write("red");
		results.write(";");
		if len(meta_sub1[i]) != 0:
			results.write(meta_sub1[i]);
		results.write(",");

	for i in range(11):
		results.write(meta_player2[i].encode('utf-8'));
		results.write(";");
		if meta_yellow2[i] == "true":
			results.write("yellow");
		results.write(";");
		if meta_red2[i] == "true":
			results.write("red");
		results.write(";");
		if len(meta_sub2[i]) != 0:
			results.write(meta_sub2[i]);
		results.write(",");

	for i in range(11,len(meta_player1)):
		results.write(meta_player1[i].encode('utf-8'));
		results.write(";");
		if meta_yellow1[i] == "true":
			results.write("yellow");
		results.write(";");
		if meta_red1[i] == "true":
			results.write("red");
		results.write(";");
		if len(meta_sub1[i]) != 0:
			results.write(meta_sub1[i]);
		results.write(",");

	for i in range(11,len(meta_player2)):
		results.write(meta_player2[i].encode('utf-8'));
		results.write(";");
		if meta_yellow2[i] == "true":
			results.write("yellow");
		results.write(";");
		if meta_red2[i] == "true":
			results.write("red");
		results.write(";");
		if len(meta_sub2[i]) != 0:
			results.write(meta_sub2[i]);
		results.write(",");

	results.write('\n');
	time.sleep(1);

urlFile.close();
results.close();




