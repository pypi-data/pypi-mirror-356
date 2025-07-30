"""
siamese-prototype v2.0: A production-ready, asynchronous rule engine.
"""
from .engine import RuleEngine
from .core import Variable, Term, PrologError, UnificationError

__version__ = "2.0.0"
__all__ = ["RuleEngine", "Variable", "Term", "PrologError", "UnificationError"] 