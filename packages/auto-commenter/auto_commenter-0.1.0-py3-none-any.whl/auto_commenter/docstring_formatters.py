def formater(func_name, args, return_type):
    """Format the docstring in Google-style format"""
    return f"""
    def {func_name}({', '.join(args)}):
        \"\"\" 
        Description of {func_name}.
        Args:
            {', '.join([f'{arg}: type' for arg in args])}
        Returns:
            {return_type}
        \"\"\"
    """


class GoogleStyleFormatter:
    pass


def formatter(func_name, args, return_type):
    """Format the docstring in PEP257-style format"""
    return f"""
    def {func_name}({', '.join(args)}):
        \"\"\" 
        {func_name} function does something.

        Args:
            {', '.join([f'{arg}: type' for arg in args])}

        Returns:
            {return_type}
        \"\"\"
    """


class PEP257Formatter:
    pass