import requests
import json
import re

ROOT_URL = "https://google.com"
REGEX_URL = "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

urls_to_visit = []
urls_visited = []

from lxml import html

page = requests.get(ROOT_URL)
webpage = html.fromstring(page.content)
finds = webpage.xpath('//a/@href')
finds = [x for x in finds if x.startswith("https")]
urls_to_visit += finds
urls_visited.append(ROOT_URL)

while True:
    t_url = urls_to_visit[0]
    print(f"Visiting {t_url} and found...", end=" ")
    page = requests.get(t_url)
    webpage = html.fromstring(page.content)
    finds = webpage.xpath('//a/@href')
    print(f"{len(finds)} URLs")
    finds = [x for x in finds if x.startswith("https")]
    for url in finds:
        if url not in urls_visited:
            urls_to_visit.append(url)
    urls_visited.append(t_url)
    urls_to_visit.pop(0)