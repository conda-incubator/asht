"""Pretty printers and formatters"""
import pprint as pypprint
from collections.abc import Sequence, Mapping

from .visitors import Node, NodeVisitor


class NodePrettyFormatter(NodeVisitor):
    """Beautifully formatt a node tree"""

    def __init__(self, root=None, indent=" "):
        self.root = root
        self.indent = indent
        self._nlindent = "\n" + indent
        self._comma_nlindent = ",\n" + indent

    def visit_default(self, node):
        s = node.__class__.__name__ + "("
        if not len(node.attrs):
            return s + ")"
        attr_lines = []
        for attr in node.attrs:
            val = getattr(node, attr)
            if isinstance(val, Node):
                attr_lines.append(attr + "=" + self.visit(val).replace("\n", self._nlindent))
            elif isinstance(val, Sequence):
                attr_lines.append(attr + "=[\n")
                elems = [self.visit(x).replace("\n", self._nlindent) for x in val]
                attr_lines.append(self._comma_nlindent.join(elems))
                attr_lines.append("\n]")
            else:
                # must be basic Python type
                attr_lines.append(attr + "=" + repr(val))
        s += "\n" + self._comma_nlindent.join(attr_lines)
        s += "\n)"
        return s


def pformat_node(node, indent=" "):
    """Formats a node tree into a pretty string"""
    f = NodePrettyFormatter(indent=indent)
    s = f.visit(node)
    return s


def pformat(tree, **kwargs):
    """Formats a tree of any type into a pretty string."""
    if isinstance(tree, Node):
        s = pformat_node(tree, **kwargs)
    elif isinstance(tree, Mapping):
        s = pypprint.pformat(tree, **kwargs)
    else:
        raise TypeError("type of tree not supported: " + str(type(tree)))
    return s


def pprint(tree, sep=' ', end='\n', file=None, flush=False, **kwargs):
    """Pretty prints a tree."""
    print(pformat(tree, **kwarg), sep=sep, end=end, file=file, flush=flush)
