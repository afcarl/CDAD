#!/usr/bin/env python

import unittest
from doc_crawler import DocCrawler
from os import listdir

TEST_FOLDER = "test_docs"

class FolderFillingTest(unittest.TestCase):
  def setUp(self):
    self.crawler = DocCrawler(TEST_FOLDER)

  def test_folder_not_empty(self):
    pre_crawl = len(listdir(TEST_FOLDER))
    self.crawler.crawl_search_page("CMS")
    post_crawl = len(listdir(TEST_FOLDER))
    self.assertTrue(post_crawl > pre_crawl)
  
if __name__ == "__main__":
  unittest.main()

