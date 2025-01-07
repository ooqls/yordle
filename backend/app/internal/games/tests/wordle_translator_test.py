import unittest
from internal.games.wordle_translator import WordleTranslator

class WordleTranslatorTest(unittest.TestCase):
  def test_translate(self):
    trans = WordleTranslator()
    (guess, colors, correct) = trans.translate("TEST", "BBBB")
    self.assertEqual(len(colors), 4)
    self.assertFalse(correct)
    self.assertEqual(guess, "BBBB")
    
    (guess, colors, correct) = trans.translate("TEST", "TEST")
    self.assertEqual(len(colors), 4)
    self.assertTrue(correct)
    self.assertEqual(guess, "TEST")
    
    