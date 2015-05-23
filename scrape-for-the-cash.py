from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
from datetime import date, timedelta
import csv
import sys


BASE_URL = "http://streak.espn.go.com/en/"

def get_matchups(matchup_date_url):
	html = urlopen(matchup_date_url).read()
	soup = BeautifulSoup(html, "lxml")
	matchups = soup.findAll("div", attrs={'class': 'matchup-container'})
	return { "matchups": matchups }

f = open(sys.argv[1], 'wt')
try: 
	writer = csv.writer(f)
	writer.writerow( ('Date', 'Matchup #', 'Sport', 'Matchup Time', 'Winner %'))

	days_to_get = int(sys.argv[2])
	while days_to_get > 0:
		count = 1
		selectedDate = date.today() - timedelta(days=days_to_get)
		selectedDate = selectedDate.strftime('%Y%m%d')
		daily_results = get_matchups(BASE_URL + "?date=" + selectedDate)
		for matchup in daily_results["matchups"]:
			sport = matchup.find("div", attrs={'class': 'sport-description'})
			matchupDate = matchup.find("span", attrs={'class': 'startTime'})
			winning_tr = matchup.findAll("img")
			if len(winning_tr) > 1:
				winner = winning_tr[1] #TODO: fails when a push exists
				winning_pct = winner.find_parent("span").find_parent('td').find_parent('tr').find("span", attrs={'class': 'wpw'})
				writer.writerow( (selectedDate, str(count), sport.string, matchupDate.string, winning_pct.string))
				count += 1
		days_to_get -= 1
		sleep(1)
finally:
	f.close()

print open(sys.argv[1], 'rt').read()