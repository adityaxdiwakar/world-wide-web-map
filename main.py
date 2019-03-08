import requests
import json
import re
import threading

ROOT_URL = "https://google.com"
REGEX_URL = "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

urls_to_visit = json.load(open("to_visit.json", "r"))
urls_visited = json.load(open("visited.json", "r"))



from lxml import html

page = requests.get(ROOT_URL)
webpage = html.fromstring(page.content)
finds = webpage.xpath('//a/@href')
finds = [x for x in finds if x.startswith("https")]
urls_to_visit += finds
urls_visited.append(ROOT_URL)

def check_url(index):
    while True:
        t_url = urls_to_visit[index]
        print(f"[{len(urls_visited)}] Visiting {t_url} and found...", end=" ")
        page = requests.get(t_url)
        webpage = html.fromstring(page.content)
        finds = webpage.xpath('//a/@href')
        print(f"{len(finds)} URLs, total: {len(urls_to_visit)}")
        finds = [x for x in finds if x.startswith("https")]
        for url in finds:
            if url not in urls_visited:
                urls_to_visit.append(url)
        urls_visited.append(t_url)
        urls_to_visit.pop(index)


thread1 = threading.Thread(target=check_url, args=[0])
thread2 = threading.Thread(target=check_url, args=[-1])
thread1.start()
thread2.start()

while True:
    if len(urls_visited) % 50 == 0:
        urls_to_visit = list(set(urls_to_visit))
        json.dump(
            urls_to_visit,
            open("to_visit.json", "w"),
            indent =4
        )
        json.dump(
            urls_visited,
            open("visited.json", "w"),
            indent = 4
        )