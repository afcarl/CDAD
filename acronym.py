
# various acronym processing tools used in offline and online processes
import re

CONTEXT_W = 15  # number of words on both sides of acronym for context
ACRONYM_REGEX = re.compile(r'((?:[A-Z]\.){2,}|[A-Z]{2,})\s+\([A-Za-z ]+\)')

class Acronym:

  # can be given a directory where the corpus documents are stored.  
  # The corpus is optional if you want to use this module for online 
  # processing.  
  def __init__(self, corpus = ""):
    self.corpus = corpus

  def __remove_periods__(self, instr):
    return instr.replace(".", "")

  # Find all the acronyms in a given string of text.
  # Retruns a list of the acronyms.
  def extract_acronyms(self, in_text):
    # regular expressions should match: CMS or C.M.S.
    matches = re.findall(r'(?:[A-Z]\.){2,}|[A-Z]{2,}', in_text)
    return map(self.__remove_periods__, matches)

  # Finds any in-line definitions of acronyms.  An example of this is: AI 
  # (Artificial Intelligence).  Returns a list of acronym, defintion pairs. 
  def extract_acronym_defs(self, in_text):
    r = []
    match = ACRONYM_REGEX.search(in_text, 0)
    while match != None:
      ac_meaning_str = match.group()
      ac = match.groups()[0]                         # get acronym matched
      meaning_str = ac_meaning_str[len(ac):].strip() # remove acronym str
      meaning_str = meaning_str[1:-1]                # remove parens
      r.append( (ac.replace(".", ""), meaning_str) )
      match = ACRONYM_REGEX.search(in_text, match.end())

    return r


  # given a valid corpus, return a set of words commonly "near" the acronym 
  def harvest_context(self, in_text, acronym_str):
    pass

  # see below for pseudo code
  def __scan_docs__(self):
    pass

  # iterate over the documents in the corpus and calculate the popularity
  # the return value is a float.
  def calc_acronym_popularity(self, acronym_str, doc_arr):
    pass
  
  # iterate over the dict of acronym dicts and merge meanings that are close.
  # There is nothing returned as you can modify dicts in place in Python.  
  def deduplicate(self, in_dict):
    pass

  # Given an acronym_str and a context decided the best possible meaning. 
  # Return a list of dicts with scores, the list should be sorted from 
  # highest to lowest score.  
  def rank_meanings(self, acronym_str, context):
    pass

  # see below for pseudo code
  def __calc_pop_pack__(self):
    pass

  # Runs the complete backend processing, creates a serialized dict which can
  # be loaded by the online component.  
  def create_acronym_dict(self):
    # -pseudo code for __scan_docs__:
    # the following three steps can be done in one pass through the corpus.
    # extract acronyms from every document
    # extract acronym meanings from every document
    # extract acronym context from every document 

    # pseudo code for __calc_pop_pack__
    # calucate acronym popularity (should be able to do this over the above
    # results without going through all the docs again.)  Append popularity
    # scores to resulting dict.  
    # As each result is calculated pack into a dict, where the key is the 
    # acronym and the value is a list of dicts, containing: popularity score,
    # and meaning candidates.  

    # de duplicate acronyms (same as above should be able to use results 
    # without going back to documents.)  

    # serialze data dict with acronyms, in JSON so other apps can load it. 
    pass

  def test_acronym_extraction(self):

    test_text = "I am listening to RR (Ryan Renolds)" 
    acs = m.extract_acronyms(test_text)
    assert acs == ["RR"], "failed simple extract acronym"

    test_text = "I am listening to R.R. (Rick Ross)"
    acs = m.extract_acronyms(test_text)
    assert acs == ["RR"], "failed to extract acronym with periods"

  def test_extract_acronym_defs(self):
    test_text = "I am listening to R.R. (Rick Ross)"
    meaning = m.extract_acronym_defs(test_text)
    assert meaning == [("RR", "Rick Ross")], "failed simple meaning extraction"

    test_text = "I am listening to RR (Ryan Renolds) and R.R. (Rick Ross)" 
    meaning = m.extract_acronym_defs(test_text)
    assert meaning == [("RR", "Ryan Renolds"), ("RR", "Rick Ross")], 
         "failed multiple meaning extraction"
  
if __name__ == "__main__":
  m = Acronym()

  print "running tests"
  m.test_acronym_extraction()
  m.test_extract_acronym_defs()

