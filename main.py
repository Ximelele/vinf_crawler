import Crawler

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


    web_crawler = Crawler.WebCrawler(starting_urlFandom, allowed_domainFandom, user_agent,"https://dota2.fandom.com", regexFandom, "robots.txt")

    web_crawler.web_crawler()
    # web_crawler(starting_url, allowed_domain,user_agent, "https://www.dotabuff.com", regex, "robots2.txt")
    # web_crawler(starting_urlFandom, allowed_domainFandom, user_agent, "https://dota2.fandom.com", regexFandom,"robots.txt")
    # # web_crawler(starting_urlFandom, allowed_domainFandom, user_agent, "https://dota2.fandom.com", regexFandom, "crawled","robots.txt")
