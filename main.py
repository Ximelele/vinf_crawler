import os

import Crawler


def fandom_helper() -> set:
    links_for_fandom = set()

    for filename in os.listdir('dotabuff/'):
        new_name = filename.split('_')
        if len(new_name) > 1:
            new_name = new_name[1].replace('-', '_').capitalize().split('_')
            new_name[-1] = new_name[-1].capitalize()
            new_name = "/wiki/"+'_'.join(new_name).split('.')[0]

            links_for_fandom.add(new_name)
    links_for_fandom.remove("/wiki/Natures_Prophet")
    #tvorcovia stranky maju autizmus
    links_for_fandom.add("/wiki/Nature%27s_Prophet")
    links_for_fandom.remove("/wiki/Anti_Mage")
    links_for_fandom.add("/wiki/Anti-Mage")

    return links_for_fandom


if __name__ == "__main__":
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

    web_crawler = Crawler.WebCrawler(starting_urlFandom, allowed_domainFandom, user_agent, "https://dota2.fandom.com",
                                     regexFandom, "robots.txt", fandom_helper())
    # print()

    # web_crawler.web_crawler()
    web_crawler.crawlFandomCounters()
    # web_crawler(starting_url, allowed_domain,user_agent, "https://www.dotabuff.com", regex, "robots2.txt")
    # web_crawler(starting_urlFandom, allowed_domainFandom, user_agent, "https://dota2.fandom.com", regexFandom,"robots.txt")
    # # web_crawler(starting_urlFandom, allowed_domainFandom, user_agent, "https://dota2.fandom.com", regexFandom, "crawled","robots.txt")

    #
    # print(new_name)
