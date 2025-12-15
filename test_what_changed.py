import unittest
from what_changed import split_paragraphs

class TestWhatChanged(unittest.TestCase):
    def test_split_paragraphs(self):
        text = "Para 1.\n\nPara 2.\n\nPara 3."
        paragraphs = split_paragraphs(text)
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0], "Para 1.")
        self.assertEqual(paragraphs[1], "Para 2.")
        self.assertEqual(paragraphs[2], "Para 3.")

if __name__ == '__main__':
    unittest.main()
