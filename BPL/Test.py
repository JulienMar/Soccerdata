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

print(clean_team)

players = soup.find_all('ul', class_ = "player-list")

players = [str(x) for x in players]
players = [re.sub(r'\([^)]*\)', '', y) for y in players]
players = [re.sub('<[^<]+?>', '', y) for y in players]
players = [s.split() for s in players]
players = [ x for y in players for x in y]

players = [y for y in players if not y.isdigit() and y != 'Booked']

print(players)

