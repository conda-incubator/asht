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
                setattr(self, key, value)
        if "lineno" in kwargs:
            self.lineno = kwargs["lineno"]
        if "column" in kwargs:
            self.column = kwargs["column"]
        if (set(kwargs.items()) - self.attrs) - LINE_COL:
            extra = (set(kwargs.items()) - self.attrs) - LINE_COL
            raise RuntimeError(
                "unknown attributes of node " +
                self.__class__.__name__ + ": " + repr(extra)
            )

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        for attr in self.attrs:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        from .pretty import pformat_node

        return pformat_node(self)


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


class String(Node):
    """An interpolated string made up of sub-string parts

    Attributes
    ----------
    parts : list of nodes
        Expressions that resolve the substring.
    """
    attrs = frozenset(["parts"])


class RawString(Node):
    """A literal string

    Attributes
    ----------
    value : str
        A literal string value
    """
    attrs = frozenset(["value"])


class Var(Node):
    """A variable

    Attributes
    ----------
    name : str
        The name of a variable to look up.
    """
    attrs = frozenset(["name"])


class EnvVar(Node):
    """An environment variable

    Attributes
    ----------
    name : str
        The name of an environment variable to look up.
    """
    attrs = frozenset(["name"])


class StdIn(Node):
    """A node representing the standard input stream."""


class StdOut(Node):
    """A node representing the standard output stream."""


class StdErr(Node):
    """A node representing the standard error stream."""


class Command(Node):
    """An environment variable

    Attributes
    ----------
    args : list of nodes
        The arguments to of the command.
    stdin : node
        A node representing where the stdin stream is read from.
    stdout : node
        A node representing where the stdout stream is written to.
    stderr : node
        A node representing where the stderr stream is written to.
    background : bool
        A flag for whether the command should be run in the background
    """
    attrs = frozenset([
        "args",
        "stdin",
        "stdout",
        "stderr",
        "background",
    ])
    stdin = StdIn()
    stdout = StdOut()
    stderr = StdErr()
    background = False


class BinOp(Node):
    """Generic binary operator between two nodes"""
    attrs = frozenset(["lhs", "rhs"])


class And(BinOp):
    """Logical 'and' operation (&&).

    Attributes
    ----------
    lhs : node
        The left-hand side of the operation.
    rhs : node
        The right-hand side of the operation.
    """

class Or(BinOp):
    """Logical 'or' operation (||).

    Attributes
    ----------
    lhs : node
        The left-hand side of the operation.
    rhs : node
        The right-hand side of the operation.
    """


class Not(Node):
    """Negation operator for a node

    Attributes
    ----------
    node : node
        The node to negate
    """
    attrs = frozenset(["node"])

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


class EnvDelete(Statement):
    """Removal statement for normal variable

    Attributes
    ----------
    name : str
        The name of the variable
    """
    attrs = frozenset(["name"])


class Pass(Statement):
    """Non-executing statement that is a syntatic placeholder."""


class If(Statement):
    """If-else if-else statement

    Attributes
    ----------
    test : Node
        A condition that evaluates to true or false when executed.
    body : iterable of Nodes
        The block that executes when the test resolves as true.
    orelse : iterable of Nodes
        The block that executes when the test resolves as false.
    """
    attrs = frozenset(["test", "body", "orelse"])


class For(Statement):
    """A basic loop structure

    Attributes
    ----------
    target : Node
        The loop variable to assign when iterating.
    iter : Node
        The expression to iterate over.
    body : iterable of Nodes
        The block that executes when looping
    """
    attrs = frozenset(["target", "iter", "body"])
