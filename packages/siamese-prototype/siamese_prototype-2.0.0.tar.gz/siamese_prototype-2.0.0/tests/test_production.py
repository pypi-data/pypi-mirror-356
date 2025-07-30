import pytest
import pytest_asyncio
from siamese import RuleEngine
from loguru import logger

@pytest_asyncio.fixture
async def production_engine():
    """Create a rule engine with production knowledge base."""
    engine = RuleEngine()
    engine.configure_logging(level="INFO")
    
    try:
        engine.load_from_file("tests/production_knowledge.yaml")
        logger.success("Production knowledge base loaded successfully")
        return engine
    except Exception as e:
        logger.error(f"Failed to load knowledge base: {e}")
        pytest.fail(f"Failed to load knowledge base: {e}")

@pytest.mark.asyncio
async def test_user_permissions(production_engine):
    """Test user permission rules."""
    engine = production_engine
    # Test alice (admin, active)
    assert await engine.exists("can_place_order", "alice")
    assert await engine.exists("can_view_all_orders", "alice")
    assert await engine.exists("can_approve_orders", "alice")
    
    # Test bob (user, active)
    assert await engine.exists("can_place_order", "bob")
    assert not await engine.exists("can_view_all_orders", "bob")
    assert await engine.exists("can_approve_orders", "bob")
    
    # Test charlie (user, suspended)
    assert not await engine.exists("can_place_order", "charlie")
    assert not await engine.exists("can_view_all_orders", "charlie")
    assert await engine.exists("can_approve_orders", "charlie")
    
    # Test david (manager, active)
    assert await engine.exists("can_place_order", "david")
    assert not await engine.exists("can_view_all_orders", "david")
    assert await engine.exists("can_approve_orders", "david")

@pytest.mark.asyncio
async def test_product_availability(production_engine):
    """Test product availability rules."""
    engine = production_engine
    # Available products
    assert await engine.exists("product_available", "laptop")
    assert await engine.exists("product_available", "phone")
    assert await engine.exists("product_available", "chair")
    
    # Unavailable product
    assert not await engine.exists("product_available", "book")

@pytest.mark.asyncio
async def test_order_validation(production_engine):
    """Test order validation rules."""
    engine = production_engine
    # Test order1 (alice, pending, $2400)
    assert await engine.exists("can_place_specific_order", "alice", "order1")
    assert not await engine.exists("order_requires_approval", "order1")
    assert not await engine.exists("order_auto_approved", "order1")
    
    # Test order2 (bob, completed, $800)
    assert not await engine.exists("can_place_specific_order", "bob", "order2")
    assert not await engine.exists("order_requires_approval", "order2")
    assert await engine.exists("order_auto_approved", "order2")
    
    # Test order3 (charlie, cancelled, $150)
    assert not await engine.exists("can_place_specific_order", "charlie", "order3")
    assert not await engine.exists("order_requires_approval", "order3")
    assert await engine.exists("order_auto_approved", "order3")

@pytest.mark.asyncio
async def test_discount_calculation(production_engine):
    """Test discount calculation rules."""
    engine = production_engine
    # Test admin discount
    discount_info = await engine.query_one("user_discount", "alice", "?Discount")
    assert discount_info is not None
    assert discount_info['?Discount'] == 0.1
    
    # Test manager discount
    discount_info = await engine.query_one("user_discount", "david", "?Discount")
    assert discount_info is not None
    assert discount_info['?Discount'] == 0.05
    
    # Test user discount (no discount)
    discount_info = await engine.query_one("user_discount", "bob", "?Discount")
    assert discount_info is not None
    assert discount_info['?Discount'] == 0

@pytest.mark.asyncio
async def test_inventory_checks(production_engine):
    """Test inventory sufficiency rules."""
    engine = production_engine
    # Sufficient inventory
    assert await engine.exists("sufficient_inventory", "laptop", 1)
    assert await engine.exists("sufficient_inventory", "phone", 30)
    
    # Insufficient inventory
    assert not await engine.exists("sufficient_inventory", "laptop", 60)
    assert not await engine.exists("sufficient_inventory", "book", 1)

@pytest.mark.asyncio
async def test_data_validation(production_engine):
    """Test data validation rules."""
    engine = production_engine
    # Valid prices
    assert await engine.exists("valid_product_price", 50)
    assert await engine.exists("valid_product_price", 1000)
    
    # Invalid prices
    assert not await engine.exists("valid_product_price", 0)
    assert not await engine.exists("valid_product_price", 100000)
    assert not await engine.exists("valid_product_price", 200000)

@pytest.mark.asyncio
async def test_complex_queries(production_engine):
    """Test complex query capabilities."""
    engine = production_engine
    # Test finding available products
    available_products = []
    async for sol in engine.query("product_available", "?Product"):
        available_products.append(sol['?Product'])
    
    assert "laptop" in available_products
    assert "phone" in available_products
    assert "chair" in available_products
    assert "book" not in available_products

@pytest.mark.asyncio
async def test_async_builtin(production_engine):
    """Test async built-in functionality."""
    engine = production_engine
    # Test external API call
    api_result = await engine.query_one("http_get_json", "https://httpbin.org/get", "?Response")
    assert api_result is not None
    response = api_result['?Response']
    assert isinstance(response, dict)
    assert 'origin' in response 