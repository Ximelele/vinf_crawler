import os
import re

class Cleaner:
    def __init__(self):
        pass

    def openFile(self, file):
        with open(file, 'r') as f:
            html_content = f.read()
        return html_content

    def fandomCounter(self):
        # fandom counter regex window
        pattern = r'<[^>]*\sid="Bad_against..."[^>]*>(.*?)<!--'

        directory = 'dotafandom/'
        test =  os.listdir(directory)
        for i in test:
            if re.match(r'.*_Counters.html$', i):
                file_path = os.path.join(directory, i)
                file = self.openFile(file_path)
                matches = re.search(pattern, file, re.DOTALL)
                if matches:
                    content_between_tags = matches.group(1)
                html_tags_pattern = r'<[^>]+>'

                html_content_without_tags = re.sub(html_tags_pattern, '', content_between_tags)

                file_path = os.path.join('cleaned/', i)
                html_content_without_tags = html_content_without_tags.splitlines()
                hero_sections = [i.strip() for i in html_content_without_tags]
                with open(file_path, 'w') as f:
                    for items in hero_sections:
                        f.write(items)
                        f.write('\n')
