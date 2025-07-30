import sys
import yaml
from typing import Any, List, Tuple, AsyncGenerator, Dict, Optional
from loguru import logger
from .core import Variable, Term, Rule, TraceEvent, PrologError
from .knowledge import KnowledgeBase
from .resolver import Resolver
from .unification import Unificator
from .builtins import DEFAULT_BUILTINS, AsyncBuiltin

# Helper to make dicts/lists/sets hashable for solution uniqueness
def make_hashable(obj):
    if isinstance(obj, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, (list, tuple, set)):
        return tuple(make_hashable(x) for x in obj)
    else:
        return obj

class RuleEngine:
    """
    A high-level, asynchronous facade for the Prolog engine.
    Manages knowledge, logging, configuration, and query execution.
    """
    def __init__(self, builtins: Optional[Dict[str, AsyncBuiltin]] = None):
        self.kb = KnowledgeBase()
        self.builtins = DEFAULT_BUILTINS.copy()
        if builtins:
            self.builtins.update(builtins)
        self.configure_logging(level="INFO") # Default logging level

    def configure_logging(self, level="INFO", sink=sys.stderr):
        """Configures the Loguru logger for the engine."""
        logger.remove()
        logger.add(sink, level=level, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
        logger.info("Logger configured.")

    def _to_internal(self, term_data: Any) -> Any:
        if isinstance(term_data, str) and term_data.startswith("?"):
            return Variable(term_data)
        if isinstance(term_data, (list, tuple)):
            name, *args = term_data
            if not isinstance(name, str):
                raise PrologError(f"Predicate name must be a string, got {name}")
            return Term(name, tuple(self._to_internal(arg) for arg in args))
        return term_data

    def load_from_file(self, filepath: str):
        """Loads facts and rules from a YAML file."""
        logger.info(f"Loading knowledge base from '{filepath}'...")
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
            
            for fact_data in data.get('facts', []):
                self.add_fact(*fact_data)
            
            for rule_data in data.get('rules', []):
                self.add_rule(tuple(rule_data['head']), [tuple(b) for b in rule_data['body']])
            logger.success(f"Knowledge base loaded successfully.")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {filepath}")
            raise
        except (yaml.YAMLError, KeyError, TypeError) as e:
            logger.error(f"Error parsing YAML file '{filepath}': {e}")
            raise PrologError(f"Invalid format in {filepath}") from e

    def add_fact(self, name: str, *args: Any):
        self.kb.add_fact(Term(name, tuple(self._to_internal(arg) for arg in args)))

    def add_rule(self, head_tuple: Tuple, body_tuples: List[Tuple]):
        head = self._to_internal(head_tuple)
        body = [self._to_internal(b) for b in body_tuples]
        self.kb.add_rule(Rule(head, body))

    async def query(
        self,
        name: str,
        *args: Any,
        max_solutions: int = -1,
        max_depth: int = 25,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Asynchronously queries the knowledge base. This is the main entry point.
        """
        initial_goal = self._to_internal((name, *args))
        query_vars = {arg for arg in initial_goal.args if isinstance(arg, Variable)}

        resolver = Resolver(self.kb, self.builtins)
        solution_count = 0
        unique_solutions = set()

        async for result in resolver.prove([initial_goal], max_depth=max_depth):
            if isinstance(result, TraceEvent):
                self._log_trace(result)
                continue

            solution_bindings = result
            final_solution = {
                var.name: Unificator.substitute(var, solution_bindings)
                for var in query_vars
            }
            
            frozen_solution = frozenset((k, make_hashable(v)) for k, v in final_solution.items())
            if frozen_solution not in unique_solutions:
                unique_solutions.add(frozen_solution)
                yield final_solution
                solution_count += 1
                if max_solutions != -1 and solution_count >= max_solutions:
                    logger.debug(f"Reached max solutions ({max_solutions}). Stopping.")
                    return

    async def query_one(self, name: str, *args: Any, **kwargs) -> Optional[Dict[str, Any]]:
        """Convenience method to get the first solution or None."""
        async for solution in self.query(name, *args, max_solutions=1, **kwargs):
            return solution
        return None

    async def exists(self, name: str, *args: Any, **kwargs) -> bool:
        """Convenience method to check if at least one solution exists."""
        return await self.query_one(name, *args, **kwargs) is not None

    def _log_trace(self, event: TraceEvent):
        """Uses Loguru to log a trace event."""
        indent = "  " * event.depth
        goal_str = str(event.goal)
        log_map = {
            "CALL": (logger.trace, f"CALL: {indent}{goal_str}"),
            "EXIT": (logger.success, f"EXIT: {indent}{goal_str}"),
            "FAIL": (logger.warning, f"FAIL: {indent}{goal_str}"),
        }
        log_func, msg = log_map.get(event.type, (logger.info, "TRACE: " + str(event)))
        log_func(msg) 