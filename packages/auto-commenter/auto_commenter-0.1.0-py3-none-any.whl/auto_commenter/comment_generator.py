import ast

class CommentGenerator:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)

    def generate_docstring(self, node):
        """Generate a docstring for functions or classes"""
        if isinstance(node, ast.FunctionDef):
            # Guess argument types and return type (for now, it's basic type inference)
            arg_types = [f"{arg.arg}: {self.guess_type(arg)}" for arg in node.args.args]
            return_type = self.guess_return_type(node)

            return f"""
            def {node.name}(self, {', '.join([arg.arg for arg in node.args.args])}):
                \"\"\" 
                {node.name} function description.
                Args: {', '.join(arg_types)}
                Returns: {return_type}
                \"\"\"
                pass
            """
        elif isinstance(node, ast.ClassDef):
            return f"""
            class {node.name}:
                \"\"\" 
                {node.name} class description.
                \"\"\"
                pass
            """
        return ""

    def guess_type(self, arg):
        type_map = {
            'num': 'int',
            'text': 'str',
            'data': 'dict',
            'items': 'list',
            'value': 'float'
        }

        if 'df' in arg.arg.lower():
            return 'pd.DataFrame'

        if 'arr' in arg.arg.lower() or 'array' in arg.arg.lower():
            return 'np.ndarray'

        if arg.annotation:
            if isinstance(arg.annotation, ast.Subscript):
                return self.guess_type_from_subscript(arg.annotation)
            elif isinstance(arg.annotation, ast.Name):
                return arg.annotation.id

        return type_map.get(arg.arg.lower(), 'Any')

    def guess_type_from_subscript(self, annotation):
        if isinstance(annotation.slice, ast.Index):
            if isinstance(annotation.slice.value, ast.Name):
                return annotation.slice.value.id
        return "Any"

    def guess_return_type(self, node):
        if isinstance(node.body[-1], ast.Return):
            return_node = node.body[-1].value
            if isinstance(return_node, ast.Constant):
                if isinstance(return_node.value, (int, float)):
                    return 'int' if isinstance(return_node.value, int) else 'float'
                elif isinstance(return_node.value, str):
                    return 'str'
                elif isinstance(return_node.value, bool):
                    return 'bool'
            elif isinstance(return_node, ast.List):
                return 'list'
            elif isinstance(return_node, ast.Dict):
                return 'dict'

            if isinstance(return_node, ast.Call):
                if isinstance(return_node.func, ast.Attribute) and return_node.func.attr == 'DataFrame':
                    return 'pd.DataFrame'

            if isinstance(return_node, ast.Call):
                if isinstance(return_node.func, ast.Attribute) and return_node.func.attr == 'array':
                    return 'np.ndarray'

            if isinstance(return_node, ast.Name):
                return "Any"

        return "None"

    def generate_comments(self):
        """Generate comments for code"""
        comments = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                docstring = self.generate_docstring(node)
                comments.append(docstring)
        return comments