"""Bash tools."""
from .visitors import DictVisitor, STDIN_DICT, STDOUT_DICT, STDERR_DICT

class ToFishFromDict(DictVisitor):
    """Coverts dict tree to Fish code."""

    def visit_Script(self, dct):
        return "".join(map(self.visit, dct["Script"]["body"]))

    def visit_Comment(self, dct):
        return "# " + dct["Comment"]["value"] + "\n"

    def visit_String(Self, dct):
        s = '"' + "".join(map(self.visit, dct["String"]

    def visit_RawString(self, dct):
        return dct["RawString"]["value"]

    def visit_Var(self, dct):
        #TODO: Check if fish really refers to things this way
        return dct["Var"]["name"]

    def visit_EnvVar(self, dct):
        return dct["EnvVar"]["nam"]

    def visit_UniversalEnvAssign(self, dct):
        #TODO: See how this is integrated
        #universal variables persist over reboots
        return "set -Ux " + dct["EnvVar"]["name"] 

    def visit_GlobalEnvVarAssign(self, dct):
        #TODO: See how this is integrated in Fish
        #Global Variabls do not persist over reboots
        return "set -g -x " + dct["EnvVar"]["name"]

    def visit_ScopedEnvVarAssign(self, dct):
        #TODO: See how to set this within function
        return "set -x " + dct["EnvVar"]["name"]

    def visit_Command(self, dct):
        #TODO: Research and clarify
        pass

    def visit_And(self, dct):
        # This really isn't and, but a compare in fish.
        s = self.visit(dct["And"]["lhs"]) + "-a" + self.visit(dct["And"]["rhs"])
        return s

    def visit_AndNum(self, dct):
        # This is also just a hacky, temp solution -- compare Numbers
        s = self.visit(dct["And"]["lhs"]) + "-eq" + self.visit(dct["And"]["rhs"])

    def visit_Assign(self, dct):
        attrs = dct["Assign"]
        return attrs["name"] + "=" + self.visit(attrs["value"]) + "\n"

    def visit_Delete(self, dct):
        return "set -e " + dct["Delete"]["name"] + "\n"

    def visit_EnvDelete(self, dct):
        return "set -e " + dct["EnvDelete"]["name"] + "\n"

    def visit_Pass(self, dct):
        pass

    def visit_If(self, dct):
        pass

    def visit_For(self, dict):
        pass
