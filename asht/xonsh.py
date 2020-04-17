"""Xonsh tools."""
from .nodes import Node
from .visitors import DictVisitor, STDIN_DICT, STDOUT_DICT, STDERR_DICT, NodeToDict


class ToXonshFromDict(DictVisitor):
    """Converts dict tree to Xonsh code."""

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
        return dct["Var"]["name"]

    def visit_EnvVar(self, dct):
        return "$" + dct["EnvVar"]["name"]

    def visit_Command(self, dct):
        attrs = next(iter(dct.values()))
        s = " ".join(map(self.visit, attrs["args"]))
        if "stderr" in attrs and attrs["stderr"] != STDERR_DICT:
            s += " e> " + self.visit(attrs["stderr"])
        if "stdout" in attrs and attrs["stdout"] != STDOUT_DICT:
            s += " > " + self.visit(attrs["stdout"])
        if "stdin" in attrs and attrs["stdin"] != STDIN_DICT:
            s += " < " + self.visit(attrs["stdin"])
        if "background" in attrs and attrs["background"]:
            s += " &"
        return "![" + s + "]"

    def visit_CapturedCommand(self, dct):
        return "$(" + self.visit_Command(dct)[2:-1] + ")"

    def visit_And(self, dct):
        s = self.visit(dct["And"]["lhs"]) + " and " + self.visit(dct["And"]["rhs"])
        return s

    def visit_Or(self, dct):
        s = self.visit(dct["Or"]["lhs"]) + " or " + self.visit(dct["Or"]["rhs"])
        return s

    def visit_Not(self, dct):
        return "not " + self.visit(dct["Not"]["node"])

    def visit_Statement(self, dct):
        return self.visit(dct["Statement"]["node"]) + "\n"

    def visit_Assign(self, dct):
        attrs = dct["Assign"]
        return attrs["name"] + " = " + self.visit(attrs["value"]) + "\n"

    def visit_Delete(self, dct):
        return "del " + dct["Delete"]["name"] + "\n"

    def visit_EnvAssign(self, dct):
        attrs = dct["EnvAssign"]
        s = "$" + attrs["name"] + " = " + self.visit(attrs["value"]) + "\n"
        return s

    def visit_EnvDelete(self, dct):
        return "del $" + dct["EnvDelete"]["name"] + "\n"

    def visit_AliasAssign(self, dct):
        attrs = dct["AliasAssign"]
        s = 'aliases["' + attrs["name"] + '"] = ' + self.visit(attrs["value"]) + "\n"
        return s

    def visit_AliasDelete(self, dct):
        return 'del aliases["' + dct["AliasDelete"]["name"] + '"]\n'

    def visit_Pass(self, dct):
        return "pass\n"

    def visit_If(self, dct):
        attrs = dct["If"]
        s = "if " + self.visit(attrs["test"]) + ":\n"
        s += "    " + "    ".join(map(self.visit, attrs["body"]))
        orelse = attrs.get("orelse", None)
        if not orelse:
            pass
        elif len(orelse) == 1 and next(iter(orelse[0].keys())) == "If":
            s += "el" + self.visit_If(orelse[0])
        else:
            s += "else:\n"
            s += "    " + "    ".join(map(self.visit, orelse))
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
        s += self.visit(attrs["iter"]) + ":\n"
        s += "    " + "    ".join(map(self.visit, attrs["body"]))
        return s

    def visit_Function(self, dct):
        s = "def " + dct["Function"]["name"] + "():\n"
        s += "    " + "    ".join(map(self.visit, dct["Function"]["body"]))
        return s


def toxonsh(tree):
    """Converts a tree to Xonsh."""
    if isinstance(tree, Node):
        todict = NodeToDict()
        tree = todict.visit(tree)
    visitor = ToXonshFromDict()
    return visitor.visit(tree)
