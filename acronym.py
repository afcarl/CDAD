
# various acronym processing tools used in offline and online processes

CONTEXT_W = 15  # number of words on both sides of acronym for context

class Acronym:

  # can be given a directory where the corpus documents are stored.  
  # The corpus is optional if you want to use this module for online 
  # processing.  
  def __init__(self, corpus = ""):
    self.corpus = corpus

  # Find all the acronyms in a given string of text.
  # Retruns a list of the acronyms.
  def extract_acronyms(in_text, self):
    # regular expressions should match: CMS or C.M.S.
    pass

  # Finds any in-line definitions of acronyms.  An example of this is: AI 
  # (Artificial Intelligence).  Returns a list of acronym, defintion pairs. 
  def extract_acronym_defs(in_text, self):
    # regular expressions should match: CMS (Content Management System) 
    pass

  # given a valid corpus, return a set of words commonly "near" the acronym 
  def harvest_context(in_text, acronym_str, self):
    pass

  # see below for pseudo code
  def __scan_docs__(self):
    pass

  # iterate over the documents in the corpus and calculate the popularity
  # the return value is a float.
  def calc_acronym_popularity(acronym_str, doc_arr, self):
    pass
  
  # iterate over the dict of acronym dicts and merge meanings that are close.
  # There is nothing returned as you can modify dicts in place in Python.  
  def deduplicate(in_dict, self):
    pass

  # Given an acronym_str and a context decided the best possible meaning. 
  # Return a list of dicts with scores, the list should be sorted from 
  # highest to lowest score.  
  def rank_meanings(acronym_str, context, self):
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
  
if __name__ == "__main__":

  print "working on it bro"
