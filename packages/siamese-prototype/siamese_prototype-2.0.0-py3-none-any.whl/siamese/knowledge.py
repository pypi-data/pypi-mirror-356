import collections
from typing import List, Dict, Tuple
from .core import Term, Rule, Goal

class KnowledgeBase:
    """Stores facts and rules, and provides indexing for fast retrieval."""
    def __init__(self):
        self.facts: List[Term] = []
        self.rules: List[Rule] = []
        self._fact_index: Dict[Tuple[str, int], List[Term]] = collections.defaultdict(list)
        self._rule_index: Dict[Tuple[str, int], List[Rule]] = collections.defaultdict(list)

    def add_fact(self, fact: Term):
        if fact not in self.facts:
            self.facts.append(fact)
            self._fact_index[(fact.name, len(fact.args))].append(fact)

    def add_rule(self, rule: Rule):
        self.rules.append(rule)
        self._rule_index[(rule.head.name, len(rule.head.args))].append(rule)

    def find_facts(self, goal: Goal) -> List[Term]:
        return self._fact_index.get((goal.name, len(goal.args)), [])

    def find_rules(self, goal: Goal) -> List[Rule]:
        return self._rule_index.get((goal.name, len(goal.args)), []) 