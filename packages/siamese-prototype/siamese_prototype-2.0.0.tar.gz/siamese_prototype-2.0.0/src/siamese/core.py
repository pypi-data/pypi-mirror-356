from collections import namedtuple
from typing import Any

# Custom exceptions
class PrologError(Exception): pass
class UnificationError(PrologError): pass

# Core data types
class Variable:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.startswith("?"):
            raise TypeError("Variable name must be a string starting with '?'")
        self.name = name
    def __repr__(self) -> str: return f"Var({self.name})"
    def __eq__(self, other) -> bool: return isinstance(other, Variable) and self.name == other.name
    def __hash__(self) -> int: return hash(self.name)

Term = namedtuple("Term", ["name", "args"])
Rule = namedtuple("Rule", ["head", "body"])
TraceEvent = namedtuple("TraceEvent", ["type", "depth", "goal"])

# Type Aliases
Bindings = dict[Variable, Any]
Goal = Term 