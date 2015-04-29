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

if __name__ == "__main__":
  unittest.main()

