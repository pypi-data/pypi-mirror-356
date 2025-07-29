import ast

class CodeAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)

    def analyze(self):
        """Analyze code and provide necessary information"""
        functions = []
        classes = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
            elif isinstance(node, ast.ClassDef):
                classes.append(node)

        return {"functions": functions, "classes": classes}