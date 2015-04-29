#!/usr/bin/env python

import unittest
from acronym import Acronym
from os import listdir

TEST_FOLDER = "test_docs"

class FolderFillingTest(unittest.TestCase):
  def setUp(self):
    self.ac = Acronym(TEST_FOLDER)

  def test_folder_not_empty(self):
    self.assertTrue(True)
  
if __name__ == "__main__":
  unittest.main()

