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
        test = os.listdir(directory)
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

    def fandomLore(self):
        directory = 'dotafandom/'
        pattern = r'<div style=\"font-style:italic; font-size:13px;\">(.*?</div>)'
        test = os.listdir(directory)
        for i in test:
            if re.match(r'.*Lore.html$', i):
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

    def fandomBugs(self):
        pattern = r'<div style=\"flex: 1 1 500px;\">(.*?</div>)\n.*\n(.*?)</span></div>'
        directory = 'dotafandom/'
        test = os.listdir(directory)
        for i in test:

            if re.match(r'.*Bugs.html$', i):
                file_path = os.path.join(directory, i)
                # file_path = 'dotafandom/wiki_Abaddon_Bugs.html'
                file = self.openFile(file_path)
                matches = re.findall(pattern, file)

                if matches:
                    html_tags_pattern = r'<[^>]+>'
                    content_between_tags: list = []
                    content_between_tags_time: list = []
                    for j in matches:
                        content_between_tags.append(re.sub(html_tags_pattern, '', j[0]))
                        content_between_tags_time.append(re.sub(html_tags_pattern, '', j[1]))
                file_path = os.path.join('cleaned/', i)
                with open(file_path, 'w') as f:
                    for one, two in zip(content_between_tags, content_between_tags_time):
                        f.write(one)
                        f.write('\n')
                        f.write(two)
                        f.write('\n\n')

    def fandomTalents(self):
        pattern = r'(Hero\sTalents(.*\n){5}</tbody>)'
        directory = 'dotafandom/'
        test = os.listdir(directory)
        for i in test:

            if re.match(r'.*Talents.html$', i):
                file_path = os.path.join(directory, i)
                file = self.openFile(file_path)
                matches = re.search(pattern, file)

                if matches:
                    html_tags_pattern = r'<[^>]+>'
                    cleaned_matches = re.sub(r' {1,}', ' ', str(re.sub(html_tags_pattern, ' ', matches.group(1))))
                file_path = os.path.join('cleaned/', i)
                with open(file_path, 'w') as f:
                    f.write(cleaned_matches)
