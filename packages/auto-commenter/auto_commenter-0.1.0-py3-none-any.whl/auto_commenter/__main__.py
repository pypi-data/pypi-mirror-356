from auto_commenter import CommentGenerator
import os

def process_code():
    # Sample Python code to be processed
    code = """
def example_function(a, b):
    result = a + b
    if result > 10:
        return result
    else:
        return result * 2
    """

    generator = CommentGenerator(code)

    # Generate comments (docstrings)
    comments = generator.generate_comments()

    # Output generated comments to console (or process further)
    print("\n".join(comments))

if __name__ == "__main__":
    process_code()