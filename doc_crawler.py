#!/usr/bin/env pytho

# stand alone module for crawling and scraping SimplyHired.com
# http://www.simplyhired.com/search?q=EMR
# produces a "corpus" in the corpus folder of plan text documents.
# this only needs to be run one time.  

from urllib2 import urlopen
from bs4 import BeautifulSoup
from time import sleep
from os import listdir
import codecs 

ROOT_URL = "http://www.simplyhired.com/search?q="

class DocCrawler():
  def __init__(self, corpus):
    self.corpus = corpus
    self.max_pages = 1

    # this code makes sure we don't overwrite existing files in the corpus
    file_list = sorted(listdir(self.corpus), reverse=True)

    if len(file_list) == 0: self.last_file_id = 0
    else:
      self.last_file_id = int(file_list[0].split('.')[0])
    print "the last file number is: %d" % self.last_file_id

  # writes the text to the next available file name
  def __write_to_next_doc__(self,doc_text):
    print "writing to file"
    suffix = "{0:05d}.txt".format(self.last_file_id)
    fw = codecs.open("{}/{}".format(self.corpus, suffix), "w", "utf-8")
    fw.write(doc_text)
    fw.close()
    self.last_file_id += 1

  # This method crawls the results of a SimplyHired search.
  # We can use top-level domain information to get the relevant content
  # The main text is contained in div with the class: js-description-full
  def crawl_result_page(self, url):
    print "fetching: %s" % url
    try:
      c = urlopen(url)
      text = c.read()
      soup = BeautifulSoup(text)
      job_descr = soup.find("div", "js-description-full")
      self.__write_to_next_doc__(job_descr.text)
      print "\t\tsucessful"
      sleep(10)
      return True
    except:
      print "\t\tERROR"
      sleep(10)
      return False


  def abs_link(self, job_soup):
    job_links = job_soup.find_all('a')
    return job_links[-1]['href']

  # open a search page for the search_str on SimplyHired
  # pages beyond the first have the pn=page_num argument
  # http://www.simplyhired.com/search?q=Kentico+CMS&pn=2
  def crawl_search_page(self, search_str):
    print "fetching results for %s" % search_str
    c = urlopen("%s%s" % (ROOT_URL, search_str))
    text = c.read()
    soup = BeautifulSoup(text)
    # get all list items (li) with class="result"
    # the results are very rich with information such as location state/city
    # Some of the jobs may be duplicates because multiple staffing firma, in
    # the future it would be good to deduplicate these.
    jobs = soup.find_all('li', "result")
    job_links = map(self.abs_link, jobs)
    crawls = map(self.crawl_result_page, job_links)
  
  
if __name__ == "__main__":
  crawler = DocCrawler("docs")

  #seed_acronyms = ["EMR", "POS", "CMS", "CRM"]
  crawler.crawl_search_page("CMS")
  #map(crawler.crawl_search_page, seed_acronyms)

  print "finished crawling"
