import pytest
import pytest_asyncio
from siamese import RuleEngine
from loguru import logger

@pytest_asyncio.fixture
async def fibonacci_engine():
    """Create a rule engine with Fibonacci rules."""
    engine = RuleEngine()
    engine.configure_logging(level="INFO")
    
    # Add Fibonacci facts and rules directly to the engine
    logger.info("Setting up Fibonacci rules...")
    
    # Base cases
    engine.add_fact("fib", 0, 0)
    engine.add_fact("fib", 1, 1)
    
    # Recursive rule: fib(N, F) :- N > 1, N1 is N-1, N2 is N-2, fib(N1, F1), fib(N2, F2), F is F1 + F2
    # We'll break this down into simpler steps
    
    # Step 1: Calculate N-1
    engine.add_rule(
        ("fib_prev1", "?N", "?N1"),
        [
            ("gt", "?N", 1),
            ("sub", "?N", 1, "?N1")
        ]
    )
    
    # Step 2: Calculate N-2
    engine.add_rule(
        ("fib_prev2", "?N", "?N2"),
        [
            ("gt", "?N", 1),
            ("sub", "?N", 2, "?N2")
        ]
    )
    
    # Step 3: Main Fibonacci rule
    engine.add_rule(
        ("fib", "?N", "?F"),
        [
            ("gt", "?N", 1),
            ("fib_prev1", "?N", "?N1"),
            ("fib_prev2", "?N", "?N2"),
            ("fib", "?N1", "?F1"),
            ("fib", "?N2", "?F2"),
            ("add", "?F1", "?F2", "?F")
        ]
    )
    
    logger.success("Fibonacci rules set up successfully")
    return engine

@pytest.mark.asyncio
async def test_fibonacci_base_cases(fibonacci_engine):
    """Test Fibonacci base cases (0 and 1)."""
    engine = fibonacci_engine
    # Test fib(0) = 0
    result = await engine.query_one("fib", 0, "?F")
    assert result is not None
    assert result['?F'] == 0
    
    # Test fib(1) = 1
    result = await engine.query_one("fib", 1, "?F")
    assert result is not None
    assert result['?F'] == 1

@pytest.mark.asyncio
async def test_fibonacci_small_numbers(fibonacci_engine):
    """Test Fibonacci for small numbers."""
    engine = fibonacci_engine
    expected_values = {
        2: 1,
        3: 2,
        4: 3,
        5: 5
    }
    
    for n, expected in expected_values.items():
        result = await engine.query_one("fib", n, "?F")
        assert result is not None, f"Failed to calculate fib({n})"
        assert result['?F'] == expected, f"fib({n}) = {result['?F']}, expected {expected}"

@pytest.mark.asyncio
async def test_fibonacci_recursive_steps(fibonacci_engine):
    """Test that Fibonacci recursive steps work correctly."""
    engine = fibonacci_engine
    # Test fib_prev1 and fib_prev2 for n=4
    n1_result = await engine.query_one("fib_prev1", 4, "?N1")
    n2_result = await engine.query_one("fib_prev2", 4, "?N2")
    
    assert n1_result is not None
    assert n2_result is not None
    assert n1_result['?N1'] == 3
    assert n2_result['?N2'] == 2
    
    # Verify that fib(4) = fib(3) + fib(2)
    fib3_result = await engine.query_one("fib", 3, "?F1")
    fib2_result = await engine.query_one("fib", 2, "?F2")
    
    assert fib3_result is not None
    assert fib2_result is not None
    assert fib3_result['?F1'] == 2
    assert fib2_result['?F2'] == 1
    assert fib3_result['?F1'] + fib2_result['?F2'] == 3

@pytest.mark.asyncio
async def test_fibonacci_large_number_fails_due_to_depth_limit(fibonacci_engine):
    """Test that large Fibonacci numbers fail due to depth limit (expected behavior)."""
    engine = fibonacci_engine
    # This should fail due to recursive depth limit
    result = await engine.query_one("fib", 15, "?F")
    assert result is None, "Large Fibonacci calculation should fail due to depth limit" 