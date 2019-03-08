import requests
import json
import re
import threading

ROOT_URL = "https://google.com"
REGEX_URL = "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

from lxml import html

def get_visited():
    return json.load(open("visited.json", "r"))

def get_to_visit():
    return json.load(open("to_visit.json", "r")) 

def push_visited(data):
    json.dump(data, 
                       open("visited.json", "w"),
                       indent = 1)

def push_to_visit(data):
    json.dump(data, 
                       open("to_visit.json", "w"),
                       indent = 1)

def append_to_visit(url):
    to_visit = get_to_visit()
    to_visit.append(url)
    push_to_visit(to_visit)

def append_visited(url):
    visited = get_visited()
    visited.append(url)
    push_visited(visited)

def check_for_visitation(url):
    if url in get_visited():
        return False
    return True

def check_for_queued_visit(url):
    if url in get_to_visit():
        return False
    return True

def queue_pop(index):
    to_visit = get_to_visit()
    to_visit.pop(index)
    push_to_visit(to_visit)

while True:
    try:
        t_url = get_to_visit()[0]

        print(f"[{len(get_visited())}] Visiting {t_url} and found...", end=" ")
        page = requests.get(t_url)
        webpage = html.fromstring(page.content)
        finds = webpage.xpath('//a/@href')
        print(f"{len(finds)} URLs, total: {len(get_to_visit())}")

        finds = [x for x in finds if x.startswith("https")]

        for url in set(list(finds)):
            if check_for_queued_visit(url):
                if check_for_visitation(url):
                    append_to_visit(url)

        append_visited(t_url)
    except:
        print("Something went wrong")
    queue_pop(0)