"""Node and dictionary visitors"""

class NodeVisitor:
    """Base node visitor class"""

    def __init__(self, root=None):
        """
        Parameters
        ----------
        node : Node or None
        """
        self.root = root

    def visit(self, node=None):
        """Visit the tree or node"""
        node = self.root if node is None else node
        meth_name = "visit_" + node.__class__.__name__
        meth = getattr(self, meth_name, self.visit_default)
        rtn = meth(node)
        return rtn

    def visit_default(self, node):
        raise NotImplementedError(
            self.__class__.__name__ +
            " does not implement visit_default() or visit_" +
            self.__class__.__name__ +
            "()."
        )


class NodeToDict(NodeVisitor):
    """Creates a dictionary representation of nodes."""

    def visit_Script(self, node):
        return {"Script": {"body": list(map(self.visit, node.body))}}

    def visit_Comment(self, node):
        return {"Comment": {"value": node.value}}

    def visit_String(self, node):
        return {"String": {"parts": list(map(self.visit, node.parts))}}

    def visit_RawString(self, node):
        return {"RawString": {"value": node.value}}

    def visit_Var(self, node):
        return {"Var": {"name": node.name}}

    def visit_EnvVar(self, node):
        return {"EnvVar": {"name": node.name}}

    def visit_StdIn(self, node):
        return {"StdIn": {}}

    def visit_StdOut(self, node):
        return {"StdOut": {}}

    def visit_StdErr(self, node):
        return {"StdErr": {}}

    def visit_Command(self, node):
        return {"Command": {
            "args": list(map(self.visit, node.args)),
            "stdin": self.visit(node.stdin),
            "stdout": self.visit(node.stdout),
            "stderr": self.visit(node.stderr),
            "background": node.background,
        }}

    def visit_BinOp(self, node):
        return {node.__class__.__name__: {
            "lhs": node.lhs,
            "rhs": node.rhs,
        }}

    visit_And = visit_BinOp
    visit_Or = visit_BinOp

    def visit_Not(self, node):
        return {"Not": {"node": self.visit(node)}}

    def visit_Statement(self, node):
        return {"Statement": {"node": self.visit(node)}}

    def visit_Assign(self, node):
        return {"Assign": {
            "name": node.name,
            "value": self.visit(node.value),
            "scope": node.scope,
        }}

    def visit_EnvAssign(self, node):
        return {"EnvAssign": {
            "name": node.name,
            "value": self.visit(node.value),
        }}

    def visit_Delete(self, node):
        return {"Delete": {"name": node.name}}

    def visit_EnvDelete(self, node):
        return {"EnvDelete": {"name": node.name}}

    def visit_Pass(self, node):
        return {"Pass": {}}

    def visit_If(self, node):
        return {"If": {
            "test": self.visit(node.test),
            "body": list(map(self.visit, node.body)),
            "orelse": list(map(self.visit, node.orelse)),
        }}

    def visit_For(self, node):
        return {"For": {
            "target": self.visit(node.target),
            "iter": self.visit(node.iter),
            "body": list(map(self.visit, node.body)),
        }}

class DictVisitor:
    """Base dict visitor class"""

    def __init__(self, root=None):
        """
        Parameters
        ----------
        root : dict or None
        """
        self.root = root

    def visit(self, dct=None):
        """Visit the tree or dict"""
        dct = self.root if node is None else dct
        meth_name = "visit_" + next(iter(dct))
        meth = getattr(self, meth_name, self.visit_default)
        rtn = meth(dct)
        return rtn

    def visit_default(self, dct):
        raise NotImplementedError(
            self.__class__.__name__ +
            " does not implement visit_default() or visit_" +
            next(iter(dct)) +
            "()."
        )


class DictToNode(DictVistor):
    """Creates a node tree representation from a dict"""