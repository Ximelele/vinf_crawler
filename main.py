import os
import Crawler

import re
import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import MMapDirectory, NIOFSDirectory
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause

import unittest


class TestSearchQuery(unittest.TestCase):

    def setUp(self):
        self.current_test_name = self.id().split('.')[-1]

    def test_abbadon_couters_in_docs(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        searchTerm = "Abaddon counters"
        term_query = QueryParser("content", analyzer).parse(searchTerm)
        max_results = 20
        top_docs: IndexSearcher = searcher.search(
            term_query, max_results).scoreDocs
        doc_id = top_docs[0].doc
        self.assertEqual(doc_id, 363)

    def test_term_not_in_docs(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        searchTerm = "Ferko Mrkvicka na hrade"
        term_query = QueryParser("content", analyzer).parse(searchTerm)
        max_results = 20
        top_docs: IndexSearcher = searcher.search(
            term_query, max_results).scoreDocs
        self.assertEqual(len(top_docs), 0)

    def test_right_input_wrong_doc(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        searchTerm = "Abaddon counter"
        term_query = QueryParser("content", analyzer).parse(searchTerm)
        max_results = 20
        top_docs: IndexSearcher = searcher.search(
            term_query, max_results).scoreDocs
        doc_id = top_docs[0].doc
        self.assertNotEqual(doc_id, 363)

    def test_right_input_correct_doc_bool(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        boolean_query = BooleanQuery.Builder()

        name_query = QueryParser("content", analyzer).parse('Slark')
        boolean_query.add(name_query, BooleanClause.Occur.MUST)
        name_query = QueryParser("content", analyzer).parse('Disadvantage')
        boolean_query.add(name_query, BooleanClause.Occur.MUST)

        top_docs = searcher.search(boolean_query.build(), 20).scoreDocs
        doc_id = top_docs[0].doc
        self.assertEqual(doc_id, 509)

    def test_right_input_wrong_doc_bool(self):
        print(f"Running test: {self.current_test_name}")
        analyzer = StandardAnalyzer()
        directory = MMapDirectory(Paths.get(index_path))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        boolean_query = BooleanQuery.Builder()

        name_query = QueryParser("content", analyzer).parse('Axe')
        boolean_query.add(name_query, BooleanClause.Occur.MUST)
        name_query = QueryParser("content", analyzer).parse('Disadvantage')
        boolean_query.add(name_query, BooleanClause.Occur.MUST)

        top_docs = searcher.search(boolean_query.build(), 20).scoreDocs
        doc_id = top_docs[0].doc
        self.assertNotEqual(doc_id, 345)


def index_files(root_folder, index_path):

    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(NIOFSDirectory(Paths.get(index_path)), config)
    file_dir = os.listdir(root_folder)

    for file in file_dir:

        doc = Document()
        # Adding path to indexing
        doc.add(StringField("path", os.path.join(
            root_folder, file), Field.Store.YES))
        ß
        with open(os.path.join(root_folder, file), 'r') as f:
            content = f.read()
            # Adding content to indexing
            doc.add(TextField("content", content, TextField.Store.YES))

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

    # fixing differencies in naming
    links_for_fandom.remove("/wiki/Natures_Prophet")
    links_for_fandom.add("/wiki/Nature%27s_Prophet")
    links_for_fandom.remove("/wiki/Anti_Mage")
    links_for_fandom.add("/wiki/Anti-Mage")

    return links_for_fandom


def single_query():
    # setting up analyzer and searcher
    analyzer = StandardAnalyzer()
    directory = MMapDirectory(Paths.get(index_path))
    searcher = IndexSearcher(DirectoryReader.open(directory))

    searchTerm = str(input('Search phrase: '))
    term_query = QueryParser("content", analyzer).parse(searchTerm)
    max_results = 20
    # Searching using default query
    top_docs: IndexSearcher = searcher.search(term_query, max_results)

    print("[%s] = total matching documents." % len(top_docs.scoreDocs))
    for score_doc in top_docs.scoreDocs:
        doc_id = score_doc.doc
        document = searcher.doc(doc_id)
        print(f"Score: {score_doc.score} Document ID: {
              doc_id}, Path: {document.get('path')}")

    docID = int(input('Select doc: '))
    document = searcher.doc(docID)
    print(f"{document.get('path')}\n{document.get('content')}")
    searcher.getIndexReader().close()


def boolean_query_search():
    boolean_query_hint()
    # setting up analyzer and searcher
    analyzer = StandardAnalyzer()
    directory = MMapDirectory(Paths.get(index_path))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    boolean_query = BooleanQuery.Builder()
    boolstring = searchTerm = str(input('Search phrase: '))

    # separate query input on AND and NOT
    find_AND = re.findall(r'(\S+)\sAND\s(\S+)', boolstring)
    find_NOT = re.findall(r'NOT\s(\S+\s\S+|\S+)', boolstring)

    if find_AND:
        for i in find_AND[0]:
            # adding AND query to boolean query
            name_query = QueryParser("content", analyzer).parse(i)
            boolean_query.add(name_query, BooleanClause.Occur.MUST)

    if find_NOT:
        for i in find_NOT:
            # adding AND query to boolean query
            name_query = QueryParser("content", analyzer).parse(i)
            boolean_query.add(name_query, BooleanClause.Occur.MUST_NOT)

    print(find_AND)
    print(find_NOT)

    top_docs = searcher.search(boolean_query.build(), 20)
    print("[%s] = total matching documents." % len(top_docs.scoreDocs))

    for score_doc in top_docs.scoreDocs:
        doc_id = score_doc.doc
        document = searcher.doc(doc_id)
        print(f"Score: {score_doc.score} Document ID: {
              doc_id}, Path: {document.get('path')}")

    docID = int(input('Select doc: '))
    document = searcher.doc(docID)
    print(f"{document.get('path')}\n{document.get('content')}")
    searcher.getIndexReader().close()


def menu():
    print(f"""
    Press 1 for unit tests (Restart required)
    Press 2 for single query
    Press 3 for boolean query
    Press 4 for end
          """)


def boolean_query_hint():
    print(f"""
    Chaining interaction
    Example: Axe AND Abaddon NOT Disadvantage
    """)


if __name__ == "__main__":
    root_folder = "/workspaces/VINF_CRAWLER/cleaned/"
    index_path = "/workspaces/VINF_CRAWLER/index/"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    while True:
        menu()
        user_input = int(input())
        if user_input == 1:
            unittest.main()
        elif user_input == 2:
            single_query()
        elif user_input == 3:
            boolean_query_search()
        elif user_input == 4:
            break
