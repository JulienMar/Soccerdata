from lxml import html
import requests

page = requests.get('http://www.bbc.com/sport/football/premier-league/results')
tree = html.fromstring(page.text)

links = tree.xpath('//a[@class="report"]/@href')


print(len(links))