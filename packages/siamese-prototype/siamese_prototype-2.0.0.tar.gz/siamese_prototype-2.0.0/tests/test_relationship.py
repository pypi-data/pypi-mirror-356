import pytest
import pytest_asyncio
from siamese import RuleEngine
from loguru import logger

@pytest_asyncio.fixture
async def relationship_engine():
    """Create a rule engine with relationship knowledge base."""
    engine = RuleEngine()
    engine.configure_logging(level="INFO")
    engine.load_from_file("tests/relationship_knowledge.yaml")
    return engine

@pytest.mark.asyncio
async def test_parent_relationships(relationship_engine):
    """Test parent relationship queries."""
    engine = relationship_engine
    # Test alice's children
    children = []
    async for sol in engine.query("parent", "alice", "?Child"):
        children.append(sol['?Child'])
    
    assert "bob" in children
    assert "charlie" in children
    assert len(children) == 2

@pytest.mark.asyncio
async def test_ancestor_relationships(relationship_engine):
    """Test ancestor relationship queries."""
    engine = relationship_engine
    # Test grace's ancestors
    ancestors = []
    async for sol in engine.query("ancestor", "?A", "grace"):
        ancestors.append(sol['?A'])
    
    assert "bob" in ancestors
    assert "alice" in ancestors
    assert len(ancestors) == 2

@pytest.mark.asyncio
async def test_sibling_relationships(relationship_engine):
    """Test sibling relationship queries."""
    engine = relationship_engine
    # Test emily's siblings
    siblings = []
    async for sol in engine.query("sibling", "emily", "?Sib"):
        siblings.append(sol['?Sib'])
    
    assert "frank" in siblings
    assert len(siblings) == 1

@pytest.mark.asyncio
async def test_cousin_relationships(relationship_engine):
    """Test cousin relationship queries."""
    engine = relationship_engine
    # Test if grace and helen are cousins
    result = await engine.exists("cousin", "grace", "helen")
    assert result is True

@pytest.mark.asyncio
async def test_spouse_relationships(relationship_engine):
    """Test spouse relationship queries."""
    engine = relationship_engine
    # Test alice's spouse
    spouses = []
    async for sol in engine.query("spouse", "alice", "?Spouse"):
        spouses.append(sol['?Spouse'])
    
    assert "david" in spouses
    assert len(spouses) == 1

@pytest.mark.asyncio
async def test_async_builtin_in_relationship(relationship_engine):
    """Test async built-in functionality in relationship context."""
    engine = relationship_engine
    # Test person IP query (this uses http_get_json)
    sol = await engine.query_one("person_ip", "bob", "?IP")
    assert sol is not None
    assert '?IP' in sol
    assert isinstance(sol['?IP'], str)