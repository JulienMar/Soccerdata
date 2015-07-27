from lxml import html
import requests
from bs4 import BeautifulSoup
import re

#I'M AT THE SOUP STORE!
def getSoup(link):
    page = requests.get(link)
    data = page.text
    return BeautifulSoup(data, "lxml")

#Reports link: http://www.bbc.com/sport/football/premier-league/results
def getReports(scoreLinks):
    page = requests.get(scoreLinks)
    tree = html.fromstring(page.text)
    return tree.xpath('//a[@class="report"]/@href')

def matchReport(matchlink):
    link = 'http://www.bbc.com/sport/0/football/' + matchlink[-8:]
    return getSoup(link)

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

def getHomePlayers(soccerSoup):
    players = getAllPlayers(soccerSoup)
    return (players[:11])

def getAwayPlayers(soccerSoup):
    players = getAllPlayers(soccerSoup)
    return (players[11:])

def getPlayersPerTeam(soccerSoup):
    playersPerTeam = {}
    teams = getTeams(soccerSoup)
    playersPerTeam[teams[0]] = getHomePlayers(soccerSoup)
    playersPerTeam[teams[1]] = getAwayPlayers(soccerSoup)
    return playersPerTeam

def getPlayerId(playerName):
    link = "http://www.soccerwiki.org/wiki.php?action=search&searchType=all&q=" + playerName
    searchSoup = getSoup(link)
    for a in searchSoup.find_all('a', href=True):
        if "pid" in a['href']:
            return a['href']

def getPlayerCountry(playerId):
    link = "http://www.soccerwiki.org/" + playerId
    playerSoup = getSoup(link)
    return playerSoup.find('span', class_=re.compile(r"flag*"))['title']

