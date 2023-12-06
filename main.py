import os
import Crawler
# import sparkMerge
import lucene


from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField,StringField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import MMapDirectory,NIOFSDirectory
from org.apache.lucene.search import IndexSearcher
import os

import unittest

# def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
import unittest

class TestSearchQuery(unittest.TestCase):
    
    def setUp(self):
        self.current_test_name = self.id().split('.')[-1]

    def test_abbadon_couters_in_docs(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        searchTerm  = "Abaddon counters"
        term_query = QueryParser("content",analyzer).parse(searchTerm)
        max_results = 20
        top_docs: IndexSearcher = searcher.search(term_query, max_results).scoreDocs
        doc_id = top_docs[0].doc
        self.assertEqual(doc_id, 363)

    def test_term_not_in_docs(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        searchTerm  = "Ferko Mrkvicka na hrade"
        term_query = QueryParser("content",analyzer).parse(searchTerm)
        max_results = 20
        top_docs: IndexSearcher = searcher.search(term_query, max_results).scoreDocs
        self.assertEqual(len(top_docs), 0)

    def test_right_input_wrong_doc(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        searchTerm  = "Abaddon counter"
        term_query = QueryParser("content",analyzer).parse(searchTerm)
        max_results = 20
        top_docs: IndexSearcher = searcher.search(term_query, max_results).scoreDocs
        doc_id = top_docs[0].doc
        self.assertNotEqual(doc_id, 363)


def index_files(root_folder, index_path):

    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(NIOFSDirectory(Paths.get(index_path)), config)
    file_dir = os.listdir(root_folder)
    print(len(file_dir))
    for file in file_dir:

        doc = Document()
        
        doc.add(StringField("path", os.path.join(root_folder, file), Field.Store.YES))
        with open(os.path.join(root_folder, file), 'r') as f:        
            content = f.read()
            doc.add(TextField("content", content, TextField.Store.YES))
            # doc.add(Field("title", "Abbadon counter",TextField.TYPE_STORED))

            writer.addDocument(doc)



    writer.commit()
    writer.close()

def fandom_helper() -> set:
    links_for_fandom = set()

    for filename in os.listdir('dotabuff/'):
        new_name = filename.split('_')
        if len(new_name) > 1:
            new_name = new_name[1].replace('-', '_').capitalize().split('_')
            new_name[-1] = new_name[-1].capitalize()
            new_name = "/wiki/" + '_'.join(new_name).split('.')[0]



            links_for_fandom.add(new_name)
    links_for_fandom.remove("/wiki/Natures_Prophet")
    # tvorcovia stranky maju autizmus
    links_for_fandom.add("/wiki/Nature%27s_Prophet")
    links_for_fandom.remove("/wiki/Anti_Mage")
    links_for_fandom.add("/wiki/Anti-Mage")

    return links_for_fandom
def boolQuery():
    test_query = "Axe AND Doom AND Brewmaster NOT Chen"
    
    test_query = test_query.split('AND')
    print(test_query)

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

    # web_crawler = Crawler.WebCrawler(starting_url, allowed_domain, user_agent, "https://www.dotabuff.com",
    #                                         regex, "robots2.txt")
    # web_crawler.web_crawler()

    web_crawler_fandom = Crawler.WebCrawler(starting_urlFandom, allowed_domainFandom, user_agent,


                                            "https://dota2.fandom.com", regexFandom, "robots.txt", fandom_helper())

    #
    # web_crawler_fandom.web_crawler()

    # web_crawler_fandom.crawlFandomCounters()

    # web_crawler_fandom.cleaner.fandomCounter()
    # web_crawler_fandom.cleaner.fandomLore()
    # web_crawler_fandom.cleaner.fandomBugs()
    # web_crawler_fandom.cleaner.fandomTalents()

    # web_crawler_fandom.cleaner.fandomChangelog()

    # web_crawler_fandom.cleaner.fandomChangelog()
    # web_crawler_fandom.cleaner.buffCounter()


root_folder = "/workspaces/VINF_CRAWLER/cleaned/"


index_path = "/workspaces/VINF_CRAWLER/index/"


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# index_files(root_folder, index_path)

# boolQuery()

# analyzer = StandardAnalyzer()
unittest.main()
# directory = MMapDirectory(Paths.get(index_path))
# searcher = IndexSearcher(DirectoryReader.open(directory))
# searchTerm  = str(input('Search phrase: '))
# term_query = QueryParser("content",analyzer).parse(searchTerm)
# max_results = 20
# top_docs: IndexSearcher = searcher.search(term_query, max_results)

# # boolean_query = BooleanQuery.Builder()
# # name_query = QueryParser("name", analyzer).parse("Abaddon")
# # boolean_query.add(name_query, BooleanClause.Occur.MUST)

# # multiple_heroes = QueryParser("category", analyzer).parse("Axe")
# # boolean_query.add(multiple_heroes, BooleanClause.Occur.MUST)

# # results = searcher.search(boolean_query.build(), 1000)
# # # # hits = results.scoreDocs 


# print("[%s] = total matching documents." % len(top_docs.scoreDocs))


# for score_doc in top_docs.scoreDocs:
#     doc_id = score_doc.doc
#     document = searcher.doc(doc_id)
#     print(f"Score: {score_doc.score} Document ID: {doc_id}, Path: {document.get('path')}")
    
# docID  = int(input('Select doc: '))
# document = searcher.doc(docID)
# print(f"{document.get('path')}\n{document.get('content')}")
# searcher.getIndexReader().close()




# sparkMerge.mergeData()


>>>>>>> origin/main
