#!/usr/bin/env python

import unittest
from acronym import Acronym
from os import listdir

TEST_FOLDER = "test_docs"

class OfflineTest(unittest.TestCase):
  def setUp(self):
    self.ac = Acronym(TEST_FOLDER)

  def test_remove_periods(self):
    removed = self.ac.__remove_periods__("R.I.P.")
    self.assertEqual(removed, "RIP")

  def test_acronym_extraction(self):
    test_text = "I am listening to RR (Ryan Renolds)"
    acs = self.ac.extract_acronyms(test_text)
    assert acs == ["RR"], "failed simple extract acronym"

    test_text = "I am listening to R.R. (Rick Ross)"
    acs = self.ac.extract_acronyms(test_text)
    assert acs == ["RR"], "failed to extract acronym with periods"

  def test_extract_acronym_defs(self):
    test_text = "I am listening to R.R. (Rick Ross)"
    meaning = self.ac.extract_acronym_defs(test_text)
    assert meaning == [("RR", "Rick Ross")], "failed simple meaning extraction"

    test_text = "I am listening to RR (Ryan Renolds) and R.R. (Rick Ross)"
    meaning = self.ac.extract_acronym_defs(test_text)
    assert meaning == [("RR", "Ryan Renolds"), ("RR", "Rick Ross")], "failed multiple meaning extraction" 

  def test_words_match(self):
    does_it_match = self.ac.__words_match_acronym__("RN", ["Registered", "Nurse"])
    self.assertTrue(does_it_match)
    does_it_match = self.ac.__words_match_acronym__("RN", ["registered", "nurse"])
    self.assertTrue(does_it_match)

  def test_words_match_extra(self):
    does_it_match = self.ac.__words_match_acronym__("RN", ["registered", "nurse", "works"])
    self.assertTrue(does_it_match)

  def test_harvest_context(self):
    test_text = "I would go see the RR concert, I doubt that anyone has the beard of RR."
    context = self.ac.harvest_context(test_text, "RR")
    self.assertEqual(context, set(['concert', 'I', 'of', 'see', 'the', 'beard']))

  def test_num_occurances(self):
    c = self.ac.__num__occurances__("JJ", ["I love JJ", "he is JJ", "snake"])
    self.assertEqual(c, 2)

  def test_calc_acronym_popularity(self):
    d = {"ss":[{"def":""}], "JJ":[{"def":""}]}
    self.ac.calc_acronym_popularity([], d)
    self.assertEqual(d["ss"][0]["popularity"], 1.0)

if __name__ == "__main__":
  unittest.main()

