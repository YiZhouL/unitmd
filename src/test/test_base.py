import unittest

from src.unitmd.parse import MarkdownParser


class TestBase(unittest.TestCase):
    parser = MarkdownParser()

    def test_one(self):
        self.parser.convert_from_file("test.md", "test.html", standalone=True)


if __name__ == "__main__":
    unittest.main()

