from typing import AsyncGenerator, Callable
import aiohttp
from .core import Bindings, Goal, UnificationError, Variable
from .unification import Unificator

# A type alias for async built-in functions
AsyncBuiltin = Callable[[Goal, Bindings], AsyncGenerator[Bindings, None]]

async def neq_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term1 is not unifiable with term2."""
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    
    # If either term is still a variable, we can't determine inequality yet
    if isinstance(term1, Variable) or isinstance(term2, Variable):
        return
    
    # If terms are not equal, succeed
    if term1 != term2:
        yield bindings

async def eq_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term1 equals term2."""
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    
    # If either term is still a variable, we can't determine equality yet
    if isinstance(term1, Variable) or isinstance(term2, Variable):
        return
    
    # If terms are equal, succeed
    if term1 == term2:
        yield bindings

async def gt_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term1 > term2."""
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    
    if isinstance(term1, Variable) or isinstance(term2, Variable):
        return
    
    if isinstance(term1, (int, float)) and isinstance(term2, (int, float)):
        if term1 > term2:
            yield bindings

async def gte_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term1 >= term2."""
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    
    if isinstance(term1, Variable) or isinstance(term2, Variable):
        return
    
    if isinstance(term1, (int, float)) and isinstance(term2, (int, float)):
        if term1 >= term2:
            yield bindings

async def lt_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term1 < term2."""
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    
    if isinstance(term1, Variable) or isinstance(term2, Variable):
        return
    
    if isinstance(term1, (int, float)) and isinstance(term2, (int, float)):
        if term1 < term2:
            yield bindings

async def lte_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term1 <= term2."""
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    
    if isinstance(term1, Variable) or isinstance(term2, Variable):
        return
    
    if isinstance(term1, (int, float)) and isinstance(term2, (int, float)):
        if term1 <= term2:
            yield bindings

async def or_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if any of the terms in the list are true."""
    # For now, we'll implement a simple OR with two arguments
    # This can be extended to handle more arguments
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    
    # For now, we'll treat this as a simple boolean OR
    # In a more sophisticated implementation, we'd evaluate the terms as goals
    if term1 or term2:
        yield bindings

async def member_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term is a member of the list."""
    term = Unificator.substitute(goal.args[0], bindings)
    list_term = Unificator.substitute(goal.args[1], bindings)
    
    if isinstance(term, Variable) or not isinstance(list_term, list):
        return
    
    if term in list_term:
        yield bindings

async def add_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Adds two numbers and unifies with result."""
    a = Unificator.substitute(goal.args[0], bindings)
    b = Unificator.substitute(goal.args[1], bindings)
    result_var = goal.args[2]
    
    if isinstance(a, Variable) or isinstance(b, Variable):
        return
    
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        result = a + b
        new_bindings = Unificator.unify(result_var, result, bindings)
        if new_bindings:
            yield new_bindings

async def sub_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Subtracts second number from first and unifies with result."""
    a = Unificator.substitute(goal.args[0], bindings)
    b = Unificator.substitute(goal.args[1], bindings)
    result_var = goal.args[2]
    
    if isinstance(a, Variable) or isinstance(b, Variable):
        return
    
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        result = a - b
        new_bindings = Unificator.unify(result_var, result, bindings)
        if new_bindings:
            yield new_bindings

async def is_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Evaluates arithmetic expression and unifies with result."""
    expr = Unificator.substitute(goal.args[0], bindings)
    result_var = goal.args[1]
    
    if isinstance(expr, Variable):
        return
    
    try:
        # Simple arithmetic evaluation (for safety, we'll only allow basic operations)
        if isinstance(expr, (int, float)):
            result = expr
        elif isinstance(expr, str) and all(c in '0123456789+-*/(). ' for c in expr):
            result = eval(expr)
        else:
            return
        
        new_bindings = Unificator.unify(result_var, result, bindings)
        if new_bindings:
            yield new_bindings
    except:
        return

async def unify_json_path(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Extracts a value from JSON using a path and unifies it with a variable."""
    json_data = Unificator.substitute(goal.args[0], bindings)
    path = Unificator.substitute(goal.args[1], bindings)
    result_var = goal.args[2]
    
    if isinstance(json_data, Variable) or isinstance(path, Variable):
        return
    
    if not isinstance(json_data, dict) or not isinstance(path, str):
        return
    
    try:
        # Simple path extraction (for now, just direct key access)
        if path in json_data:
            value = json_data[path]
            new_bindings = Unificator.unify(result_var, value, bindings)
            if new_bindings:
                yield new_bindings
    except:
        return

async def http_get_json(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """
    Performs an async HTTP GET request and unifies the JSON response with a variable.
    Example: http_get_json('https://httpbin.org/get', ?Response)
    """
    url_term = Unificator.substitute(goal.args[0], bindings)
    result_var = goal.args[1]

    if not isinstance(url_term, str) or not isinstance(result_var, Variable):
        return # Fails if arguments are not of the correct type

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_term) as response:
                response.raise_for_status()
                json_data = await response.json()
                
                # Try to unify the fetched data with the result variable
                new_bindings = Unificator.unify(result_var, json_data, bindings)
                if new_bindings:
                    yield new_bindings
    except Exception:
        # Fails silently on any network or parsing error
        return

DEFAULT_BUILTINS: dict[str, AsyncBuiltin] = {
    "neq": neq_builtin,
    "eq": eq_builtin,
    "gt": gt_builtin,
    "gte": gte_builtin,
    "lt": lt_builtin,
    "lte": lte_builtin,
    "or": or_builtin,
    "member": member_builtin,
    "add": add_builtin,
    "sub": sub_builtin,
    "is": is_builtin,
    "unify_json_path": unify_json_path,
    "http_get_json": http_get_json,
} 