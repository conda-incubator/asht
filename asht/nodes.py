"""Abstract syntax tree nodes for a generic shell"""

LINE_COL = frozenset(["lineno", "column"])

class Node:
    """Top-level node class"""

    # maps attribute names to default value generators
    attrs = frozenset()
    lineno = 1
    column = 1

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.attrs:
                setattr(self, key, value):
        if lineno in kwargs:
            self.lineno = kwargs["lineno"]
        if column in kwargs:
            self.column = kwargs["column"]
        if (set(kwargs.items()) - self.attrs) - LINE_COL:
            extra = (set(kwargs.items()) - self.attrs) - LINE_COL
            raise RuntimeError(
                f"unknown attributes of node "
                f"{self.__class__.__name__}: {extra}"
            )


class Script(Node):
    """Represents a script in a shell language.


    Attributes
    ----------
    body : list of statements
        Statements that make up the script
    """
    attrs = frozenset(["body"])


class Comment(Node):
    """Unexecuted commentary

    Attributes
    ----------
    value : str
        The contents of the comment
    """
    attrs = frozenset(["value"])


#
# Statements
#

class Statement(Node):
    """Generic statement node

    Attributes
    ----------
    node : non-statement Node
        The node to evaluate on a line
    """
    attrs = frozenset(["node"])


class Assign(Statement):
    """Assignment statement for normal variable

    Attributes
    ----------
    name : str
        The name of the variable
    value : non-statement Node
        The value to assign to name
    scope : "local" or "global"
        A string flag indicating the scope of this variable.
    """
    attrs = frozenset(["name", "value", "scope"])


class EnvAssign(Statement):
    """Assignment statement for environment variable

    Attributes
    ----------
    name : str
        The name of the environment variable
    value : non-statement Node
        The value to assign to name
    """
    attrs = frozenset(["name", "value"])


class Delete(Statement):
    """Removal statement for normal variable

    Attributes
    ----------
    name : str
        The name of the variable
    """
    attrs = frozenset(["name"])

