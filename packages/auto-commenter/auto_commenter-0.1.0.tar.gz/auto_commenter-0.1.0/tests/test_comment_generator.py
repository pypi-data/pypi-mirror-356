import unittest
from auto_commenter.comment_generator import CommentGenerator

class TestCommentGenerator(unittest.TestCase):
    def test_generate_docstring(self):
        code = """
def my_function(x, y):
    return x + y
"""
        generator = CommentGenerator(code)
        comments = generator.generate_comments()
        self.assertTrue("my_function" in comments[0])
        self.assertTrue("Args" in comments[0])

    def test_generate_empty_function(self):
        code = """
def empty_function():
    pass
"""
        generator = CommentGenerator(code)
        comments = generator.generate_comments()
        self.assertTrue("empty_function" in comments[0])
        self.assertTrue("Args" in comments[0])
        self.assertTrue("Returns: None" in comments[0])

if __name__ == '__main__':
    unittest.main()