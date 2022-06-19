import ast
import re


class FunctionParser:
    def __init__(self, source: str, funcname: str):
        if source is None:
            raise ValueError("Source can't be none")
        if funcname is None:
            raise ValueError("Function name can't be none")
        self.source = source
        self.funcname = re.sub(r"\[\.+\]", '', funcname)
        self.function = None

    def parse(self):
        code_tree = ast.parse(self.source)
        for ast_obj in code_tree.body:
            if type(ast_obj).__name__ == 'FunctionDef':
                if ast_obj.name == self.funcname:
                    self.function = ast_obj
                    break
        if self.function is None:
            raise Exception(f"Failed to find {self.funcname} in source")
        return self

    def docstring(self):
        ast_doc = self.function.body[0]
        if type(ast_doc).__name__ != 'Expr':
            return None
        if not hasattr(ast_doc.value, "value"):
            return None
        return ast_doc.value.value

    def decorator_value(self, deconame, keyword):
        for decorator in self.function.decorator_list:
            if not hasattr(decorator, "func"):
                continue
            if decorator.func.attr == deconame:
                for k in decorator.keywords:
                    if k.arg == keyword:
                        if hasattr(k.value, "value"):
                            return k.value.value
                        elif hasattr(k.value, "s"):
                            return k.value.s
        return None

