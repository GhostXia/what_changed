import unittest
from paper_diff import split_paragraphs, compare_texts

class TestPaperDiff(unittest.TestCase):
    def test_split_paragraphs(self):
        text = "Para 1.\n\nPara 2.\n\nPara 3."
        paragraphs = split_paragraphs(text)
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0], "Para 1.")
        self.assertEqual(paragraphs[1], "Para 2.")
        self.assertEqual(paragraphs[2], "Para 3.")

    def test_compare_texts_change(self):
        text1 = "Para 1.\n\nPara 2."
        text2 = "Para 1.\n\nPara 2 changed."
        diffs = compare_texts(text1, text2)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0][0], 'change')

    def test_compare_texts_delete(self):
        text1 = "Para 1.\n\nPara 2."
        text2 = "Para 1."
        diffs = compare_texts(text1, text2)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0][0], 'delete')

    def test_compare_texts_insert(self):
        text1 = "Para 1."
        text2 = "Para 1.\n\nPara 2."
        diffs = compare_texts(text1, text2)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0][0], 'insert')

if __name__ == '__main__':
    unittest.main()
