from collections import deque
from typing import List, AsyncIterator, Dict, Callable
from .core import Rule, Bindings, Goal, Variable, Term, TraceEvent
from .knowledge import KnowledgeBase
from .unification import Unificator
from .builtins import AsyncBuiltin

class Resolver:
    """A stateless, asynchronous, iterative solver for a given query."""
    def __init__(self, kb: KnowledgeBase, builtins: Dict[str, AsyncBuiltin]):
        self.kb = kb
        self.builtins = builtins
        self._rename_counter = 0

    def _rename_term(self, term):
        self._rename_counter += 1
        rename_map: dict[Variable, Variable] = {}
        def rename(t):
            if isinstance(t, Variable):
                if t not in rename_map:
                    rename_map[t] = Variable(f"{t.name}_{self._rename_counter}")
                return rename_map[t]
            if isinstance(t, Term):
                return Term(t.name, tuple(rename(arg) for arg in t.args))
            return t
        return rename(term)

    def _rename_rule(self, rule: Rule) -> Rule:
        self._rename_counter += 1
        rename_map: dict[Variable, Variable] = {}
        
        def rename(t):
            if isinstance(t, Variable):
                if t not in rename_map:
                    rename_map[t] = Variable(f"{t.name}_{self._rename_counter}")
                return rename_map[t]
            if isinstance(t, Term):
                return Term(t.name, tuple(rename(arg) for arg in t.args))
            return t
        
        return Rule(rename(rule.head), [rename(t) for t in rule.body])

    async def prove(self, goals: List[Goal], max_depth: int) -> AsyncIterator[Bindings | TraceEvent]:
        """Asynchronous, iterative-deepening solver using a stack."""
        stack = deque([(goals, {}, 0)])

        while stack:
            current_goals, bindings, depth = stack.pop()
            
            if not current_goals:
                yield bindings
                continue

            if depth > max_depth:
                continue

            goal = Unificator.substitute(current_goals[0], bindings)
            remaining_goals = current_goals[1:]
            
            yield TraceEvent("CALL", depth, goal)
            
            provable = False
            # We create a list of potential next states to add to the stack.
            # This is because async generators can't be used in regular list comprehensions.
            next_states = []

            # 1. Try built-ins
            if goal.name in self.builtins:
                builtin_func = self.builtins[goal.name]
                async for new_bindings in builtin_func(goal, bindings):
                    provable = True
                    next_states.append((remaining_goals, new_bindings, depth))
            
            # 2. Try facts
            for fact in self.kb.find_facts(goal):
                new_bindings = Unificator.unify(goal, self._rename_term(fact), bindings)
                if new_bindings:
                    provable = True
                    next_states.append((remaining_goals, new_bindings, depth))

            # 3. Try rules
            for rule in self.kb.find_rules(goal):
                renamed_rule = self._rename_rule(rule)
                new_bindings = Unificator.unify(goal, renamed_rule.head, bindings)
                if new_bindings:
                    provable = True
                    new_goal_list = renamed_rule.body + remaining_goals
                    next_states.append((new_goal_list, new_bindings, depth + 1))
            
            if provable:
                yield TraceEvent("EXIT", depth, goal)
                # Add new states to the stack in reverse order to maintain depth-first search
                stack.extend(reversed(next_states))
            else:
                yield TraceEvent("FAIL", depth, goal) 