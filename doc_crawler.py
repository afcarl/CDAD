

# stand alone module for crawling and scraping SimplyHired.com
# http://www.simplyhired.com/search?q=EMR
# produces a "corpus" in the corpus folder of plan text documents.
# this only needs to be run one time.  

from urllib2 import urlopen
from bs4 import BeautifulSoup

ROOT_URL = "http://www.simplyhired.com/search?q="

class DocCrawler():
  def __init__(self, corpus):
    self.corpus = corpus

  # this method crawls the results of a SimplyHired search
  # we can use top-level domain information to get the relevant conent
  def crawl_result_page(self, search_str):
    pass

  def abs_link(self, job_soup):
    job_links = job_soup.find_all('a')
    return job_links[-1]['href']

  # open a search page for the search_str on SimplyHired
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
    print job_links
  
  
if __name__ == "__main__":
  crawler = DocCrawler("docs")
  crawler.crawl_search_page("EMR")

  print "finished crawling"
