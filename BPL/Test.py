from lxml import html
import requests
from bs4 import BeautifulSoup
import re

page = requests.get('http://www.bbc.com/sport/football/premier-league/results')
tree = html.fromstring(page.text)

links = tree.xpath('//a[@class="report"]/@href')

string = 'http://www.bbc.com/sport/0/football/' + links[0][-8:]

matchPage = requests.get(string)

data = matchPage.text

soup = BeautifulSoup(data, "lxml")

teams = soup.find_all("h3", class_="team-name")
clean_team = []
for x in teams:
    clean_team.append(re.sub('<[^<]+?>', '', str(x)))

all_players = soup.find_all('span', id=lambda x: x and x.startswith('player-id'))

clean_all_players = []
for y in all_players:
    clean_all_players.append(re.sub('<[^<]+?>', '', str(y)))

print(len(clean_all_players))
