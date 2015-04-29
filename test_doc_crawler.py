#!/usr/bin/env python

import unittest

  
if __name__ == "__main__":
  crawler = DocCrawler("docs")

  #seed_acronyms = ["EMR", "POS", "CMS", "CRM"]
  crawler.crawl_search_page("CMS")
  #map(crawler.crawl_search_page, seed_acronyms)

  print "finished crawling"
