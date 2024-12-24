import json
import os
import re
import time

import feedparser
from dotenv import load_dotenv
from io import BytesIO
from curl_cffi import requests

_ = load_dotenv()


feed_url = "https://www.reddit.com/r/MayonakaHeartTune.rss"
volume = 1

def update_chapter():
    rss_raw = BytesIO(requests.get(feed_url, impersonate="chrome").content)
    rss = feedparser.parse(rss_raw)

    chapters = []

    for i in range(0, 10):
        link_etc = rss['entries'][i]['content'][0]['value']

        match = re.search(r"cubari.moe/read/imgur/(\w+)", link_etc)
        if match:
            chapter_code = match.group(1)
            # break
        else:
            continue

        if not chapter_code:
            continue

        print(f"Imgur link: https://cubari.moe/read/imgur/{chapter_code}")
        
        # title = requests.get(f"https://cubari.moe/read/api/imgur/series/{chapter_code}/").json()['title']

        regex = r"Chapter (\d+) ?[.|\-:!?]? ? [.|:!?]?([^.|!?]*)"


        matches = re.search(regex, link_etc)
        chapter_number = eval(re.search(r"Chapter (\d+)", link_etc, flags=re.IGNORECASE).group(1).strip())
        try:
            chapter_title = matches.group(2).replace("'", "").replace('"', "").strip()
        except:
            chapter_title = f"Chapter {chapter_number}"
        vol = volume or chapter_number/10

        with open('chapters.json', 'r', encoding="utf8") as file:
            data = json.load(file)

        if str(chapter_number) in list(data['chapters'].keys()):
            print(f"Chapter {chapter_number} already exists")
            continue


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
        chapters.append(str(chapter_number))

    if not chapters:
        print("No new chapter")
    chapter_number = ", ch".join(chapters)

    # Create a Github instance
    os.system("git config --local user.name fenixer")
    os.system("git config --local user.email 143337992+Fenixer@users.noreply.github.com")
    os.system("git add .")
    os.system(f'git commit -m "Auto Commit: Added ch{chapter_number}"')
    os.system("git push")

    # g = Github(os.getenv("UPDATE_TOKEN"))

    # Get the repository
    # repo = g.get_repo("Fenixer/Mayonaka-Heart-Tune")

    # Get the file
    # file = repo.get_contents("chapters.json")

    # Update the file
    # repo.update_file(file.path, f"Auto Commit: Added {chapter_number or '👍'}", json.dumps(data,indent=4), file.sha)

if __name__ == "__main__":
    update_chapter()
    print("Done")
