import requests
import bs4
import re
import time
import html5lib

urlFile = open("gameURL_29-16.txt",'r');
results = open("results_29-16.csv",'w');

results.write("URL,League,Season,Fixture,Date,Stadium,Referee,Referee_ID,Team1,Team1_ID,Team1_score,Team2,Team2_ID,Team2_score,Team1_coach,Team1_coach_ID,Team2_coach,Team2_coach_ID,Team1_scorers,Team1_scoreTimes,Team2_scorers,Team2_scoreTimes,");
for i in range(1,12):

	results.write("Team1Player" + str(i) + ",");
	results.write("Team1Player" + str(i) + "_ID,");
	results.write("Team1Player" + str(i) + "_yellow,");
	results.write("Team1Player" + str(i) + "_red,");
	results.write("Team1Player" + str(i) + "_subOn,");
	results.write("Team1Player" + str(i) + "_subOff,");

for i in range(1,12):
	results.write("Team2Player" + str(i) + ",");
	results.write("Team2Player" + str(i) + "_ID,");
	results.write("Team2Player" + str(i) + "_yellow,");
	results.write("Team2Player" + str(i) + "_red,");
	results.write("Team2Player" + str(i) + "_subOn,");
	results.write("Team2Player" + str(i) + "_subOff,");

for i in range(1,16):
	results.write("Team1Sub" + str(i) + ",");
	results.write("Team1Sub" + str(i) + "_ID,");
	results.write("Team1Sub" + str(i) + "_yellow,");
	results.write("Team1Sub" + str(i) + "_red,");
	results.write("Team1Sub" + str(i) + "_subOn,");
	results.write("Team1Sub" + str(i) + "_subOff,");

for i in range(1,16):
	results.write("Team2Sub" + str(i) + ",");
	results.write("Team2Sub" + str(i) + "_ID,");
	results.write("Team2Sub" + str(i) + "_yellow,");
	results.write("Team2Sub" + str(i) + "_red,");
	results.write("Team2Sub" + str(i) + "_subOn,");
	results.write("Team2Sub" + str(i) + "_subOff,");

results.write('\n');

gameCount = 0;

while(True):
	gameURL = urlFile.readline();
	if len(gameURL) == 0: break;

	gameCount = gameCount + 1;
	print gameURL.strip();
	#gameURL = "http://calcio-seriea.net/tabellini/2001/58381/";

	#Page for each game:
	response = requests.get(gameURL);
	soup = bs4.BeautifulSoup(response.text, "html5lib");
	tables = soup.find_all('table');

	rematch_offset = 0;
	if len(tables) >= 14:
		rematch_offset = 2;

	league_plus_season = tables[6].find_all('tr')[0].find_all('td')[0].text.strip();
	meta_league = league_plus_season[0:7];
	meta_season = league_plus_season[8:];

	match_info_rows = tables[7 + rematch_offset].find_all('tr');


	meta_fixture = match_info_rows[1].text.strip();
	meta_date = match_info_rows[2].text.strip();
	meta_stadium = match_info_rows[3].text.strip();

	#Figure out that the match was not held:
	if len(match_info_rows[4].text.strip()) == 0:

		if isinstance(meta_league, unicode):
			meta_league = meta_league.encode('utf-8');

		if isinstance(meta_season, unicode):
			meta_season = meta_season.encode('utf-8');

		if isinstance(meta_fixture, unicode):
			meta_fixture = meta_fixture.encode('utf-8');

		if isinstance(meta_date, unicode):
			meta_date = meta_date.encode('utf-8');
			
		if isinstance(meta_stadium, unicode):
			meta_stadium = meta_stadium.encode('utf-8');

		results.write(gameURL.strip());
		results.write(',');
		results.write(meta_league);
		results.write(',');
		results.write(meta_season);
		results.write(',');
		results.write(meta_fixture);
		results.write(',');
		results.write(meta_date);
		results.write(',');
		results.write(meta_stadium);
		results.write('\n');
		continue;


	meta_ref = ' '.join(match_info_rows[4].text.strip()[8:].strip().split());
	meta_ref_id = match_info_rows[4].find('a')['href'].split('/')[-2];

	gameStats_rows = tables[8 + rematch_offset].find_all('tr');

	meta_team1 = gameStats_rows[0].find_all('td')[1].text.strip();
	meta_goals1 = gameStats_rows[0].find_all('td')[3].text.strip();
	meta_goals2 = gameStats_rows[0].find_all('td')[4].text.strip();
	meta_team2 = gameStats_rows[0].find_all('td')[6].text.strip();

	# team_plus_score = gameStats_rows[0].text.strip().split();

	# meta_team1 = team_plus_score[0];
	# meta_goals1 = team_plus_score[1];
	# meta_goals2 = team_plus_score[2];
	# meta_team2 = team_plus_score[3];

	meta_team1_id = gameStats_rows[0].find_all('a')[0]['href'].split('/')[-2];
	meta_team2_id = gameStats_rows[0].find_all('a')[1]['href'].split('/')[-2];

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
	meta_player1_id = [];
	meta_player2_id = [];
	meta_yellow1 = [];
	meta_yellow2 = [];
	meta_red1 = [];
	meta_red2 = [];
	meta_subon1 = [];
	meta_subon2 = [];
	meta_suboff1 = [];
	meta_suboff2 = [];

	if r_allenatore == -1:
		playerEnd = len(gameStats_rows);
	else:
		playerEnd = r_allenatore;

	#starting11:
	for i in range(r_titolari + 1, playerEnd):

		if i == r_disposizione: continue;

		fields = gameStats_rows[i].find_all('td');

		if len(fields) < 10: break;

		#players:
		meta_player1.append(fields[1].text.strip());
		meta_player2.append(fields[8].text.strip());

		if len(fields[1].text.strip()) != 0:
			meta_player1_id.append(fields[1].find('a')['href'].split('/')[-2]);
		else:
			meta_player1_id.append("");

		if len(fields[8].text.strip()) != 0:
			meta_player2_id.append(fields[8].find('a')['href'].split('/')[-2]);
		else:
			meta_player2_id.append("");




		#sub:
		if len(fields[3].text.strip()) != 0:
			if len(fields[3].find_all('img')) == 1:
				if fields[3].find('img')['alt'] == "entrato":
					meta_subon1.append(fields[3].text.strip());
					meta_suboff1.append("");
				else:
					meta_subon1.append("");
					meta_suboff1.append(fields[3].text.strip());
			elif len(fields[3].find_all('img')) == 2:
				meta_subon1.append(fields[3].text.split()[0]);
				meta_suboff1.append(fields[3].text.split()[1]);
		else:
			meta_subon1.append("");
			meta_suboff1.append("");


		if len(fields[6].text.strip()) != 0:
			if len(fields[6].find_all('img')) == 1:
				if fields[6].find('img')['alt'] == "entrato":
					meta_subon2.append(fields[6].text.strip());
					meta_suboff2.append("");
				else:
					meta_subon2.append("");
					meta_suboff2.append(fields[6].text.strip());
			elif len(fields[6].find_all('img')) == 2:
				meta_subon2.append(fields[6].text.split()[0]);
				meta_suboff2.append(fields[6].text.split()[1]);
		else:
			meta_subon2.append("");
			meta_suboff2.append("");

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
	meta_coach1_id = "";
	meta_coach2_id = "";

	if r_allenatore != -1:
		fields = gameStats_rows[r_allenatore + 1].find_all('td');
		meta_coach1 = fields[0].text.strip();
		meta_coach2 = fields[5].text.strip();
		meta_coach1_id = fields[0].find('a')['href'].split('/')[-2];
		meta_coach2_id = fields[5].find('a')['href'].split('/')[-2];

	for i in range(len(meta_player1)):
		if isinstance(meta_player1[i], unicode):
			meta_player1[i] = meta_player1[i].encode('utf-8');

	for i in range(len(meta_player2)):
		if isinstance(meta_player2[i], unicode):
			meta_player2[i] = meta_player2[i].encode('utf-8');

	for i in range(len(meta_goalscorer1)):
		if isinstance(meta_goalscorer1[i], unicode):
			meta_goalscorer1[i] = meta_goalscorer1[i].encode('utf-8');

	for i in range(len(meta_goalscorer2)):
		if isinstance(meta_goalscorer2[i], unicode):
			meta_goalscorer2[i] = meta_goalscorer2[i].encode('utf-8');

	if isinstance(meta_coach1, unicode):
		meta_coach1 = meta_coach1.encode('utf-8');

	if isinstance(meta_coach2, unicode):
		meta_coach2 = meta_coach2.encode('utf-8');

	if isinstance(meta_ref, unicode):
		meta_ref = meta_ref.encode('utf-8');

	if isinstance(meta_date, unicode):
		meta_date = meta_date.encode('utf-8');

	if isinstance(meta_stadium, unicode):
		meta_stadium = meta_stadium.encode('utf-8');

	if isinstance(meta_fixture, unicode):
		meta_fixture = " ".join(meta_fixture.encode('utf-8').split('\n'));

	results.write(gameURL.strip() );
	results.write(",");
	results.write(meta_league );
	results.write(",");
	results.write(meta_season );
	results.write(",");
	results.write(meta_fixture );
	results.write(",");
	results.write(meta_date);
	results.write(",");
	results.write(meta_stadium );
	results.write(",");
	results.write(meta_ref );
	results.write(",");
	results.write(meta_ref_id );
	results.write(",");
	results.write(meta_team1 );
	results.write(",");
	results.write(meta_team1_id );
	results.write(",");
	results.write(meta_goals1 );
	results.write(",");
	results.write(meta_team2 );
	results.write(",");
	results.write(meta_team2_id );
	results.write(",");
	results.write(meta_goals2 );
	results.write(",");

	if r_titolari == -1:
		results.write('\n')
		continue;

	results.write(meta_coach1 );
	results.write(",");
	results.write(meta_coach1_id );
	results.write(",");
	results.write(meta_coach2 );
	results.write(",");
	results.write(meta_coach2_id );
	results.write(",");
	results.write(";".join(meta_goalscorer1) );
	results.write(",");
	results.write(";".join(meta_goaltime1) );
	results.write(",");
	results.write(";".join(meta_goalscorer2) );
	results.write(",");
	results.write(";".join(meta_goaltime2) );
	results.write(",");

	for i in range(11):
		results.write(meta_player1[i] );
		results.write(",");
		results.write(meta_player1_id[i] );
		results.write(",");
		results.write(meta_yellow1[i] );
		results.write(",");
		results.write(meta_red1[i] );
		results.write(",");
		results.write(meta_subon1[i] );
		results.write(",");
		results.write(meta_suboff1[i] );
		results.write(",");

	for i in range(11):
		results.write(meta_player2[i] );
		results.write(",");
		results.write(meta_player2_id[i] );
		results.write(",");
		results.write(meta_yellow2[i] );
		results.write(",");
		results.write(meta_red2[i] );
		results.write(",");
		results.write(meta_subon2[i] );
		results.write(",");
		results.write(meta_suboff2[i] );
		results.write(",");

	for i in range(11,11 + 15):
		if i >= len(meta_player1):
			results.write(",,,,,,");
			continue;
		results.write(meta_player1[i] );
		results.write(",");
		results.write(meta_player1_id[i] );
		results.write(",");
		results.write(meta_yellow1[i] );
		results.write(",");
		results.write(meta_red1[i] );
		results.write(",");
		results.write(meta_subon1[i] );
		results.write(",");
		results.write(meta_suboff1[i] );
		results.write(",");

	for i in range(11,11 + 15):
		if i >= len(meta_player1):
			results.write(",,,,,,");
			continue;
		results.write(meta_player2[i] );
		results.write(",");
		results.write(meta_player2_id[i] );
		results.write(",");
		results.write(meta_yellow2[i] );
		results.write(",");
		results.write(meta_red2[i] );
		results.write(",");
		results.write(meta_subon2[i] );
		results.write(",");
		results.write(meta_suboff2[i] );
		results.write(",");

	results.write('\n');
	time.sleep(0.1);

	#break;

urlFile.close();
results.close();
