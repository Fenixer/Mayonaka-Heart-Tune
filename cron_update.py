import feedparser
import re
import time
import json
import requests

feed_url = "https://www.reddit.com/r/MayonakaHeartTune.rss"
volume = 1

def update_chapter():
    rss = feedparser.parse(feed_url)

    link_etc = rss['entries'][1]['content'][0]['value']


    match = re.search(r"cubari.moe/read/imgur/(\w+)", link_etc)
    if match:
        chapter_code = match.group(1)

    print(f"Imgur link: https://cubari.moe/read/imgur/{chapter_code}")
    
    title = requests.get(f"https://cubari.moe/read/api/imgur/series/{chapter_code}/").json()['title']

    regex = r"Chapter (\d+) ?[.|:!?]? ? [.|:!?]?([^.|!?]*)"


    matches = re.search(regex, title)
    chapter_number = eval(matches.group(1).strip())
    chapter_title = matches.group(2).replace("'", "").replace('"', "").strip()
    vol = volume or chapter_number/10

    with open('chapters.json', 'r', encoding="utf8") as file:
        data = json.load(file)

    if str(chapter_number) in list(data['chapters'].keys()):
        print(f"Chapter {chapter_number} already exists")
        return


    data['chapters'][chapter_number] = {
        'title': chapter_title,
        'volume': vol,
        'last_updated': int(time.time()),
        'groups': {
            '': f'/proxy/api/imgur/chapter/{chapter_code}/'
        }
    }

    with open('chapters.json', 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Updated chapter {chapter_number}")

if __name__ == "__main__":
    update_chapter()
    print("Done")
