from lxml import html
import requests
from bs4 import BeautifulSoup
import re

def getReports(scoreLinks):
    page = requests.get(scoreLinks)
    tree = html.fromstring(page.text)
    return tree.xpath('//a[@class="report"]/@href')

def matchReport(matchlink):
    link = 'http://www.bbc.com/sport/0/football' + matchlink[-8:]
    matchPage = requests.get(link)
    data = matchPage.text
    return BeautifulSoup(data, "lxml")

#First one is the home team, second one the away team
def getTeams(soccerSoup):
    teams = soccerSoup.find_all("h3", class_="team-name")
    clean_teams = []
    for x in teams:
        clean_teams.append(re.sub('<[^<]+?>', '', str(x)))
    return clean_teams

def getAllPlayers(soccerSoup):
    players = soccerSoup.find_all('ul', class_="player-list")
    players = [re.sub(r'\([^)]*\)', '', str(y)) for y in players]
    players = [re.sub('<[^<]+?>', '', y) for y in players]
    players = [s.split() for s in players]
    players = [ x for y in players for x in y]

    players = [y for y in players if not y.isdigit() and y != 'Booked']

    return players

reports = getReports('http://www.bbc.com/sport/football/premier-league/results')
oneReport = matchReport(reports[0])
print(getTeams(oneReport))
print(getAllPlayers(oneReport))