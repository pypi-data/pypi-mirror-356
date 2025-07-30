from typing import Any, Optional
from .core import Variable, Term, Bindings

class Unificator:
    """The Unificator handles term comparison and variable binding."""
    # This class remains synchronous as it's a pure CPU-bound logic operation.
    @staticmethod
    def unify(term1: Any, term2: Any, bindings: Bindings) -> Optional[Bindings]:
        b = bindings.copy()
        stack = [(term1, term2)]
        while stack:
            t1, t2 = stack.pop()
            t1 = Unificator.substitute(t1, b)
            t2 = Unificator.substitute(t2, b)
            if t1 == t2: continue
            if isinstance(t1, Variable):
                if Unificator.occurs_check(t1, t2, b): return None
                b[t1] = t2
            elif isinstance(t2, Variable):
                if Unificator.occurs_check(t2, t1, b): return None
                b[t2] = t1
            elif isinstance(t1, Term) and isinstance(t2, Term):
                if t1.name != t2.name or len(t1.args) != len(t2.args): return None
                for arg1, arg2 in zip(reversed(t1.args), reversed(t2.args)):
                    stack.append((arg1, arg2))
            else: return None
        return b

    @staticmethod
    def substitute(term: Any, bindings: Bindings) -> Any:
        if isinstance(term, Variable) and term in bindings:
            return Unificator.substitute(bindings[term], bindings)
        if isinstance(term, Term):
            return Term(term.name, tuple(Unificator.substitute(arg, bindings) for arg in term.args))
        return term

    @staticmethod
    def occurs_check(var: Variable, term: Any, bindings: Bindings) -> bool:
        term = Unificator.substitute(term, bindings)
        if var == term: return True
        if isinstance(term, Term):
            return any(Unificator.occurs_check(var, arg, bindings) for arg in term.args)
        return False 