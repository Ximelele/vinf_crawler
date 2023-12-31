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
        # Pattern to find counter window
        pattern = r'<[^>]*\sid=\"Bad_against...\"[^>]*>(.*?)<!--'

        directory = 'dotafandom/'

        test = os.listdir(directory)

        test = os.listdir(directory)

        for i in test:
            if re.match(r'.*_Counters.html$', i):
                file_path = os.path.join(directory, i)
                file = self.openFile(file_path)
                matches = re.search(pattern, file, re.DOTALL)
                if matches:
                    content_between_tags = matches.group(1)
                else:
                    continue
                # removing html tags
                html_tags_pattern = r'<[^>]+>'

                html_content_without_tags = re.sub(
                    html_tags_pattern, '', content_between_tags)

                file_path = os.path.join('cleaned/', i)
                html_content_without_tags = html_content_without_tags.splitlines()
                hero_sections = [i.strip() for i in html_content_without_tags]
                # saving raw file
                with open(file_path, 'w') as f:
                    for items in hero_sections:
                        f.write(items)
                        f.write('\n')

    def fandomLore(self):
        directory = 'dotafandom/'
        # Pattern to find information about hero lore
        pattern = r'<div style=\"font-style:italic; font-size:13px;\">(.*?</div>)'
        test = os.listdir(directory)
        for i in test:
            if re.match(r'.*Lore.html$', i):
                file_path = os.path.join(directory, i)
                file = self.openFile(file_path)
                matches = re.search(pattern, file, re.DOTALL)
                if matches:
                    content_between_tags = matches.group(1)
                # removing html tags
                html_tags_pattern = r'<[^>]+>'

                html_content_without_tags = re.sub(
                    html_tags_pattern, '', content_between_tags)
                file_path = os.path.join('cleaned/', i)
                html_content_without_tags = html_content_without_tags.splitlines()
                hero_sections = [i.strip() for i in html_content_without_tags]

                # saving raw file
                with open(file_path, 'w') as f:
                    for items in hero_sections:
                        f.write(items)
                        f.write('\n')

    def fandomBugs(self):
        # Pattern to find hero bugs
        pattern = r'<div style=\"flex: 1 1 500px;\">(.*?</div>)\n.*\n(.*?)</span></div>'
        directory = 'dotafandom/'
        test = os.listdir(directory)
        for i in test:

            if re.match(r'.*Bugs.html$', i):
                file_path = os.path.join(directory, i)
                file = self.openFile(file_path)
                matches = re.findall(pattern, file)

                if matches:
                    # removing html tags
                    html_tags_pattern = r'<[^>]+>'
                    content_between_tags: list = []
                    content_between_tags_time: list = []
                    for j in matches:
                        content_between_tags.append(
                            re.sub(html_tags_pattern, '', j[0]))
                        content_between_tags_time.append(
                            re.sub(html_tags_pattern, '', j[1]))
                file_path = os.path.join('cleaned/', i)
                # saving raw file
                with open(file_path, 'w') as f:
                    for one, two in zip(content_between_tags, content_between_tags_time):
                        f.write(one)
                        f.write('\n')
                        f.write(two)
                        f.write('\n\n')

    def fandomTalents(self):
        # Pattern to find hero Talents
        pattern = r'(Hero\sTalents(.*\n){5}</tbody>)'
        directory = 'dotafandom/'
        test = os.listdir(directory)
        for i in test:

            if re.match(r'.*Talents.html$', i):
                file_path = os.path.join(directory, i)
                file = self.openFile(file_path)
                matches = re.search(pattern, file)

                if matches:
                    # removing html tags
                    html_tags_pattern = r'<[^>]+>'
                    cleaned_matches = re.sub(r' {1,}', ' ', str(
                        re.sub(html_tags_pattern, ' ', matches.group(1))))
                file_path = os.path.join('cleaned/', i)
                with open(file_path, 'w') as f:
                    f.write(cleaned_matches)

    def fandomChangelog(self):
        # Pattern to find hero changelogs
        open_pattern = r'<div class="updatetablebody">'
        close_pattern = r'(</div>\n){4}'
        directory = 'dotafandom/'
        test = os.listdir(directory)
        for i in test:

            if re.match(r'.*Changelogs.html$', i):
                file_path = os.path.join(directory, i)
                file = self.openFile(file_path)
                # finding two types of pattern
                open_matches = re.finditer(open_pattern, file)
                close_matches = re.finditer(close_pattern, file)

                extracted_contents = []

                for open_match, close_match in zip(open_matches, close_matches):
                    # joining matches together based ond Start and End
                    start_position = open_match.end()
                    end_position = close_match.start()
                    extracted_content = file[start_position:end_position]
                    extracted_contents.append(extracted_content)
                # removing html tags
                html_tags_pattern = r'<[^>]+>'
                #  removing magic bytes from file
                garbage = r'[^\x20-\x7E\r\n]'

                for index, content in enumerate(extracted_contents):
                    extracted_contents[index] = re.sub(
                        html_tags_pattern,  '', content)
                    extracted_contents[index] = re.sub(
                        garbage, ' ', extracted_contents[index])

                file_path = os.path.join('cleaned/', i)

                with open(file_path, 'w', encoding="utf-8") as f:
                    for j in extracted_contents:
                        #  removing magic bytes from file
                        filtered_list = [
                            s for s in j if b'\xd0' not in s.encode('utf-8')]
                        f.write(filtered_list)

    def buffCounter(self):
        # Pattern to find hero couters in dotabuff
        counter_pattern = r'<section class=\"counter-outline\">(.*?<\/section>)'
        directory = 'dotabuff/'
        test = os.listdir(directory)
        # hero data
        pattern = r'<header>Matchups</header>(.*?</section>)'
        # title
        title_pattern = r'<meta property=\"og:title\" content=(.*?)/>'
        for i in test:

            if re.match(r'.*counters.*$', i):
                with open(os.path.join(directory, i), 'r') as f:
                    html_content = f.read()

                matches = re.search(pattern, html_content, re.DOTALL)
                title_match = re.match(
                    r'"([^"]+)"', re.search(title_pattern, html_content, re.DOTALL).group(1))
                cleaned_words = title_match.group(1).split()

                title = f'{cleaned_words[0]} {cleaned_words[-1]}'

                html_tags_pattern = r'<[^>]+>'
                html_content_without_tags = re.sub(
                    html_tags_pattern, ' ', matches.group(1))
                html_content_without_tags = ''.join(html_content_without_tags.replace(
                    "              ", '\n')).replace("  Dis.     ", "").splitlines()
                stripped_list = [s.strip() for s in html_content_without_tags]

                with open(os.path.join('buffcleaned/', i), 'w') as f:

                    f.writelines(title)
                    f.write('\n')
                    for j in stripped_list:
                        f.writelines(j)
                        f.write('\n')
