"""Bash tools."""
from .nodes import Node
from .visitors import DictVisitor, STDIN_DICT, STDOUT_DICT, STDERR_DICT, NodeToDict


class ToBashFromDict(DictVisitor):
    """Converts dict tree to Bash code."""

    def visit_Script(self, dct):
        return "".join(map(self.visit, dct["Script"]["body"]))

    def visit_Comment(self, dct):
        return "# " + dct["Comment"]["value"] + "\n"

    def visit_String(self, dct):
        s = '"' + "".join(map(self.visit, dct["String"]["parts"])) + '"'
        return s

    def visit_RawString(self, dct):
        return dct["RawString"]["value"]

    def visit_Var(self, dct):
        return "$" + dct["Var"]["name"]

    def visit_EnvVar(self, dct):
        return "$" + dct["EnvVar"]["name"]

    def visit_Command(self, dct):
        attrs = dct["Command"]
        s = " ".join(map(self.visit, attrs["args"]))
        if "stderr" in attrs and attrs["stderr"] != STDERR_DICT:
            s += " 2> " + attrs["stderr"]
        if "stdout" in attrs and attrs["stdout"] != STDOUT_DICT:
            s += " > " + attrs["stdout"]
        if "stdin" in attrs and attrs["stdin"] != STDIN_DICT:
            s += " < " + attrs["stdin"]
        if "background" in attrs and attrs["background"]:
            s += "  &"
        return s

    def visit_And(self, dct):
        s = self.visit(dct["And"]["lhs"]) + " && " + self.visit(dct["And"]["rhs"])
        return s

    def visit_Or(self, dct):
        s = self.visit(dct["Or"]["lhs"]) + " || " + self.visit(dct["Or"]["rhs"])
        return s

    def visit_Not(self, dct):
        return "! " + self.visit(dct["Not"]["node"])

    def visit_Statement(self, dct):
        return self.visit(dct["Statement"]["node"]) + "\n"

    def visit_Assign(self, dct):
        attrs = dct["Assign"]
        return attrs["name"] + "=" + self.visit(attrs["value"]) + "\n"

    def visit_EnvAssign(self, dct):
        attrs = dct["EnvAssign"]
        s = "export " + attrs["name"] + "=" + self.visit(attrs["value"]) + "\n"
        return s

    def visit_Delete(self, dct):
        return "unset " + dct["Delete"]["name"] + "\n"

    def visit_EnvDelete(self, dct):
        return "unset " + dct["EnvDelete"]["name"] + "\n"

    def visit_Pass(self, dct):
        return ":\n"

    def visit_If(self, dct):
        attrs = dct["If"]
        s = "if " + self.visit(attrs["test"]) + "; then\n"
        s += "  " + "  ".join(map(self.visit, attrs["body"]))
        orelse = attrs.get("orelse", None)
        if not orelse:
            s += "fi\n"
        elif len(orelse) == 1 and next(iter(orelse[0].keys())) == "If":
            s += "el" + self.visit_If(orelse[0])
        else:
            s += "else\n"
            s += "  " + "  ".join(map(self.visit, orelse))
            s += "fi\n"
        return s

    def visit_For(self, dct):
        attrs = dct["For"]
        target = attrs["target"]
        target_type, target_name = next(iter(target.items()))
        if target_type == "Var":
            target_assign = target_name["name"]
        elif target_type == "EnvVar":
            target_assign = "$" + target_name["name"]
        else:
            raise ValueError("For loop must assign to a variable name (Var)"
                             "or environment variable name (EnvVar).")
        s = "for " + target_assign + " in "
        s += self.visit(attrs["iter"]) + "; do\n"
        s += "  " + "  ".join(map(self.visit, attrs["body"]))
        s += "done\n"
        return s


def tobash(tree):
    """Converts a tree to Bash."""
    if isinstance(tree, Node):
        todict = NodeToDict()
        tree = todict.visit(tree)
    visitor = ToBashFromDict()
    return visitor.visit(tree)
