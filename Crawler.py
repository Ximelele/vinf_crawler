import os
import requests
import re
from urllib.parse import urljoin

class WebCrawler:

    def __init__(self,starting_url, allowed_domain, user_agent, prefix_domain, regex, robots , helper = None):
        self.starting_url = starting_url
        self.allowed_domain = allowed_domain
        self.user_agent = user_agent
        self.prefix_domain = prefix_domain
        self.regex = regex
        self.robots = robots
        self.helper = helper

    def can_crawl(self, url, user_agent, robots):
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

    def web_crawler(self, new_url = None, allowed_domain = None, user_agent = None, prefix_domain = None, regex = None, robots = None):
        if new_url is None:
            new_url = self.starting_url
            allowed_domain = self.allowed_domain
            user_agent = self.user_agent
            prefix_domain = self.prefix_domain
            regex = self.regex
            robots = self.robots
        visited_urls = set()  # set aby neboli duplikaty
        to_crawl = [new_url]

        while to_crawl:
            url: str = to_crawl.pop()
            if not self.can_crawl(url, user_agent, robots):
                continue

            try:
                response = requests.get(url, headers=user_agent)
                if response.status_code == 200:
                    print(f'Crawling url: {url}')
                    links = re.findall(regex, response.text)
                    if "fandom" in prefix_domain:
                        for link in links:
                            if link not in self.helper:
                                links.remove(link)


                    # # pozrie sa ci sa nachadza zakladna domena v vyextrahovanom linku
                    modified_links = [prefix_domain + link if not re.search(allowed_domain, link) else link for link in
                                      links]
                    for link in modified_links:

                        if link not in visited_urls and re.search(allowed_domain, link):
                            visited_urls.add(link)
                            if "buff" in prefix_domain:
                                to_crawl.append(link)
                            else:
                                for hero_name in self.helper:
                                    if hero_name in link:
                                        to_crawl.append(link)
                                        break

                    if "buff" in prefix_domain:
                        file_name = url.replace("https://www.dotabuff.com/", "").replace('/', '_') + '.txt'
                        file_path = os.path.join("dotabuff/", file_name)
                        with open(file_path, "w") as file:
                            file.write(response.text)
                    else:
                        file_name = url.replace("https://dota2.fandom.com/", "").replace('/', '_') + '.txt'
                        file_path = os.path.join("dotafandom/", file_name)
                        with open(file_path, "w") as file:
                            file.write(response.text)
            except Exception as e:
                print(f"An error occurred: {str(e)}")