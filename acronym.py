
# various acronym processing tools used in offline and online processes

class Acronym:

  def __init__(self, corpus = ""):
    self.corpus = corpus

  def extract_acronyms(in_text, self):
    pass

  def extract_acronym_defs(in_text, self):
    pass

  # iterate over the documents in the corpus and calculate the popularity
  # the return value is a float.
  def calc_acronym_popularity(acronym_str, self):
    pass
  
  # given a valid corpus, return a set of words commonly "near" the acronym 
  def harvest_context(acronym_str, self):
    pass

  # Given an acronym_str and a context decided the best possible meaning. 
  # Return a list of dicts with scores, the list should be sorted from 
  # highest to lowest score.  
  def rank_meanings(acronym_str, context, self):
    pass
  
if __name__ == "__main__":

  print "working on it bro"
