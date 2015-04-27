
# various acronym processing tools used in offline and online processes
import codecs
import re
from os import listdir
import json
import Levenshtein

CONTEXT_W = 15  # number of words on both sides of acronym for context
ACRONYM_REGEX = re.compile(r'((?:[A-Z]\.){2,}|[A-Z]{2,})\s+\([A-Za-z ]+\)')
CAPS2p = r'(?:[A-Z]\.){2,}|[A-Z]{2,}'  # regex pattern to find all caps words
                                         # greater than 2 characters in length

COMPARE_MIN = 0.80

AC_MAX_LEN = 5  # heursitc to filter out capatilized words 

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
    matches = re.findall(CAPS2p, in_text)
    return map(self.__remove_periods__, matches)

  # helper to see if the characters of an acronym match the first letters
  # in the previous N tokens, where N is the length of the acronym
  def __words_match_acronym__(self, ac_str, tokens):
    matches = True
    #print "comparing: ",ac_str," and ",tokens
    for i in range(len(ac_str)):
      if not ac_str[i] == tokens[i][0].upper():
        matches = False
	break

    return matches
    
  # Finds any in-line definitions of acronyms.  An example of this is: AI 
  # (Artificial Intelligence).  Returns a list of acronym, defintion pairs. 
  # Usually the defintion comes first then the acronym like: 
  # registered nurses (RN)
  # HP Application Lifecycle Management (ALM) ver 11.0+
  # related to Shared Services Framework (SSF) required
  # store Point of Sale (POS) system
  def extract_acronym_defs(self, in_text):
    r = []

    # try first type of search acronym (def)
    match = ACRONYM_REGEX.search(in_text, 0)
    while match != None:
      ac_meaning_str = match.group()
      ac = match.groups()[0]                         # get acronym matched
      meaning_str = ac_meaning_str[len(ac):].strip() # remove acronym str
      meaning_str = meaning_str[1:-1]                # remove parens
      r.append( (ac.replace(".", ""), meaning_str) )
      match = ACRONYM_REGEX.search(in_text, match.end())

    # try second type def (acronym)
    acronyms = re.findall(CAPS2p, in_text)
    word_tokens = re.findall(u"\w+", in_text)
    #print word_tokens

    # get unique acronyms to reduce computations 
    uniq_acronyms = list(set(acronyms))

    # for each acronym check if the preceding words spell out the acronym
    for ac in uniq_acronyms:
      ac_len = len(ac)
      if ac_len > AC_MAX_LEN: continue

      for ind in [i for i,x in enumerate(word_tokens) if x == ac]:
        # check if N-ac_len words match acronym 
        if ind - ac_len < 0: continue
	prev_words = word_tokens[ind - ac_len: ind]

	if self.__words_match_acronym__(ac, prev_words):
	  r.append( (ac, " ".join(prev_words)) ) 
	else: # try again with one extra word between acronym and defintion  
	  if ind - ac_len - 1 < 0: continue
	  prev_words = word_tokens[ind - ac_len - 1: ind - 1 ]
	  if self.__words_match_acronym__(ac, prev_words):
	    r.append( (ac, " ".join(prev_words)) ) 

    return r


  # given a valid corpus, return a set of words commonly "near" the acronym 
  def harvest_context(self, in_text, acronym_str):
    ret_set = set()
    word_tokens = re.findall(u"\w+", in_text)

    # iterate over every occurance of acronym_str
    for ind in [i for i,x in enumerate(word_tokens) if x == ac]:
      lowerbound = max(0, ind - CONTEXT_W)
      upperbound = min(len(word_tokens) -1, ind + CONTEXT_W + 1)
      for word in word_tokens[lowerbound:upperbound]:
        ret_set.add(word)

    return ret_set

  # see below for pseudo code
  def __scan_docs__(self):
    if not self.corpus:
      print "you need to set the folder for the corpus"
      print "this can be set in the object constructor like: o = Acronym('dir')"
      raise Exception("corpus folder not set")

    r = []; full_text = []

    files = listdir(self.corpus)
    for fn in files:  # TODO Cleanup this into map()
      fr = codecs.open("%s/%s" % (self.corpus, fn), 'r', 'utf-8')
      text = fr.read()

      # TODO cleanup, may be able to combine these two together
      acs =  self.extract_acronyms(text)
      defs =  self.extract_acronym_defs(text)
      fr.close()
      full_text.append(text)
      r.append( (acs,defs) )

    return r, full_text

  def __num__occurances__(self, meaning, doc_a):
    total = 0
    for doc in doc_a:
      if doc.find(meaning) > -1: total += 1

    return total

  # iterate over the documents in the corpus and calculate the popularity
  # the return value is a float.
  def calc_acronym_popularity(self, doc_a, d):
    for key in d.keys():
      print key
      if len(d[key]) == 1: 
	d[key][0]["popularity"] = 1.0
      else:  # more than one meaning, need to do calculations
	temp_d = {}
	total_occurances = 0
	for item in d[key]:
	  meaning = item["def"]
	  temp_d[meaning] = self.__num__occurances__(meaning, doc_a)
	  total_occurances += temp_d[meaning]

	total_occurances = float(total_occurances)
	for item in d[key]:
	  item["popularity"] = temp_d[item["def"]]/total_occurances

  # helper: merges two meanings, sums thier popularities 
  def __merge__(self, in_arr, pair):
    i0,i1 = pair
    print "merging: ",in_arr[i0]," and ",in_arr[i1]
    if in_arr[i0]["popularity"] >=  in_arr[i1]["popularity"]:
      in_arr[i0]["popularity"] += in_arr[i1]["popularity"]
      del(in_arr[i1])
    else:
      in_arr[i1]["popularity"] += in_arr[i0]["popularity"]
      del(in_arr[i0])

  def __find_inner_loop__(self, in_arr, outer_index):

    found_pair = False; inner_index = -1
    for i in range(len(in_arr)): 
      if i == outer_index: continue
      print "comparing ",in_arr[outer_index]["def"], in_arr[i]["def"]
      ratio = Levenshtein.ratio(in_arr[outer_index]["def"], in_arr[i]["def"])
      print ratio
      if ratio > COMPARE_MIN:
        found_pair = True
	inner_index = i
	break

    if found_pair: return (outer_index, inner_index)
    else: return None

  # helper tries to find a pair to merge, if none can be found
  # it returns None.  Simply iterates over pairs of items, and quits when
  # a matching pair is found.  
  def __find_merge_pair__(self, in_arr):
    if len(in_arr) < 2: return None

    found_pair = False 
    for i in range(len(in_arr)): 
      print "outer index: %d " % i
      pair = self.__find_inner_loop__(in_arr, i)
      if pair:
        found_pair = True
	break

    if found_pair: return pair
    else: return None
    
  def __merge_similar__(self, in_arr):

    pair = self.__find_merge_pair__(in_arr)
    while pair:
      self.__merge__(in_arr, pair)  
      pair = self.__find_merge_pair__(in_arr)

    return in_arr

  # iterate over the dict of acronym dicts and merge meanings that are close.
  # There is nothing returned as you can modify dicts in place in Python.  
  # This uses the Levenshtein edit distance for sting comparision.
  def deduplicate(self, in_dict):
    for key in in_dict.keys():
      defs = in_dict[key]
      if len(defs) < 2: continue

      self.__merge_similar__(defs)  # pass by ref, will delete in place

    return in_dict

  # Given an acronym_str and a context decided the best possible meaning. 
  # Return a list of dicts with scores, the list should be sorted from 
  # highest to lowest score.  
  def rank_meanings(self, acronym_str, context):
    pass

  # see below for pseudo code
  def __calc_pop_pack__(self, info_l):
    ret_d = {}
    # iterate over definitions and pack them into dict
    for doc in info_l:
      for defi_pair in doc[1]:
        acronym, defi = defi_pair
	if acronym in ret_d:
	  if not defi in ret_d[acronym]:
	    ret_d[acronym].append({"def": defi, "popularity": 0.0})
	  # get all defintions for this acronym and see if 
	else:
	  ret_d[acronym] = [{"def": defi, "popularity": 0.0}]

    return ret_d

  # Runs the complete backend processing, creates a serialized dict which can
  # be loaded by the online component.  
  def create_acronym_dict(self):
    self.__scan_docs__()
    # -pseudo code for __scan_docs__:
    # the following three steps can be done in one pass through the corpus.
    # extract acronyms from every document
    # extract acronym meanings from every document
    # extract acronym context from every document 
    extracted_info, doc_texts = self.__scan_docs__() 

    # pseudo code for __calc_pop_pack__
    # calucate acronym popularity (should be able to do this over the above
    # results without going through all the docs again.)  Append popularity
    # scores to resulting dict.  
    # As each result is calculated pack into a dict, where the key is the 
    # acronym and the value is a list of dicts, containing: popularity score,
    # and meaning candidates.  
    prepared_dict = self.__calc_pop_pack__(extracted_info)

    self.calc_acronym_popularity(doc_texts, prepared_dict)

    # de duplicate acronyms (same as above should be able to use results 
    # without going back to documents.)  
    final_dict = self.deduplicate(prepared_dict)

    # serialze data dict with acronyms, in JSON so other apps can load it. 
    fw = open("final.json", "w")
    fw.write(json.dumps(final_dict))
    fw.close()

    json.dumps(prepared_dict)

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
    assert meaning == [("RR", "Ryan Renolds"), ("RR", "Rick Ross")], "failed multiple meaning extraction"
  
if __name__ == "__main__":
  m = Acronym("docs")
  m.create_acronym_dict()

  print "running tests"
  #m.test_acronym_extraction()
  #m.test_extract_acronym_defs()

