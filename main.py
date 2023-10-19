import os
import threading
import shutil
import requests
import re
from urllib.parse import urljoin


def can_crawl(url, user_agent, robots):
    try:
        robots_url = urljoin(url, robots)
        robots_response = requests.get(robots_url)
        if robots_response.status_code == 200:
            robots_content = robots_response.text
            for line in robots_content.split('\n'):
                if line.startswith("User-agent:") and user_agent in line:
                    allow_access = True
                    for line in robots_content.split('\n'):
                        if line.startswith("Disallow:") and re.match(r"Disallow:\s*/", line):
                            allow_access = False
                    return allow_access
            return True
        else:
            return True
    except Exception as e:
        print(f"Error checking robots.txt: {str(e)}")
        return True
def web_crawler(starting_url, allowed_domain, user_agent, prefix_domain, regex, robots):
    visited_urls = set()  # set aby neboli duplikaty
    to_crawl = [starting_url]
    # prefix_domain = "https://www.dotabuff.com"
    while to_crawl:
        url : str = to_crawl.pop()
        if not can_crawl(url, user_agent, robots):
            continue

        try:
            response = requests.get(url,headers=user_agent)
            if response.status_code == 200:

                # # najde vsetko co obsahuje wiki
                # dotafandom
                # regex = r'<a[^>]*\s+href=["\'](.*?wiki/.*?)["\'][^>]*>'
                # dotabuff
                # regex = r'<a[^>]*\s+href=["\'](.*?heroes/.*?)["\'][^>]*>'
                links = re.findall(regex, response.text)
                #
                # # pozrie sa ci sa nachadza zakladna domena v vyextrahovanom linku
                modified_links = [prefix_domain + link if not re.search(allowed_domain,link) else link for link in links]
                # modified_links = soup.find_all('a')
                for link in modified_links:
                    # print(link.get('href'))
                    if link not in visited_urls and re.search(allowed_domain,link):
                        # append_to_file(link)
                        visited_urls.add(link)
                        if not re.search(r'wiki/(Module|Special|File|Template|User)',link):
                            to_crawl.append(link)

                if "buff" in prefix_domain:
                    file_name = url.replace("https://www.dotabuff.com/","").replace('/', '_') + '.txt'
                    file_path = os.path.join("dotabuff/", file_name)
                    with open(file_path, "w") as file:
                        file.write(response.text)
                else:
                    file_name = url.replace("https://dota2.fandom.com/","").replace('/', '_') + '.txt'
                    file_path = os.path.join("dotafandom/", file_name)
                    with open(file_path, "w") as file:
                        file.write(response.text)
        except Exception as e:
            print(f"An error occurred: {str(e)}")



# def download_from_file():
#     while still_crawling:

starting_urlFandom = 'https://dota2.fandom.com'
starting_url = 'https://www.dotabuff.com/heroes'

allowed_domainFandom = r'dota2\.fandom\.com/wiki/.*'
allowed_domain = r'^https://www\.dotabuff\.com/heroes/'
user_agent = {'User-Agent': "School project on STU FIIT for information retrival (xdruzbacky@stuba.sk)"}

# # najde vsetko co obsahuje wiki
# dotafandom
regexFandom = r'<a[^>]*\s+href=["\'](.*?wiki/.*?)["\'][^>]*>'
# dotabuff
regex = r'<a[^>]*\s+href=["\'](.*?heroes/.*?)["\'][^>]*>'

web_crawler(starting_url, allowed_domain,user_agent, "https://www.dotabuff.com", regex, "robots2.txt")
# web_crawler(starting_urlFandom, allowed_domainFandom, user_agent, "https://dota2.fandom.com", regexFandom,"robots.txt")
# # web_crawler(starting_urlFandom, allowed_domainFandom, user_agent, "https://dota2.fandom.com", regexFandom, "crawled","robots.txt")



