import pytest
from robosystems_mcp.database import is_write_query


@pytest.mark.parametrize(
    "query,expected",
    [
        ("MATCH (n) RETURN n", False),
        ("CREATE (n:Person) RETURN n", True),
        ("MERGE (n:Person {name: 'Alice'}) RETURN n", True),
        ("SET n.age = 30", True),
        ("DELETE n", True),
        ("REMOVE n.property", True),
        ("ADD n.list = []", True),
        ("WITH 1 as num RETURN num", False),
        ("MATCH (n) WHERE n.name = 'Alice' RETURN n", False),
        ("// Comment\nMATCH (n) RETURN n", False),
        ("CREATE /* comment */ (n:Person)", True),
        ("match (n) return n", False),  # Case insensitive test
        ("CREATE (n:Person)\nRETURN n", True),  # Multi-line test
    ],
)
def test_is_write_query(query, expected):
    assert is_write_query(query) == expected


def test_is_write_query_with_empty_string():
    assert not is_write_query("")


def test_is_write_query_with_whitespace():
    assert not is_write_query("   \n   ")


def test_is_write_query_with_comments_only():
    assert not is_write_query("// This is a comment\n/* Another comment */")


def test_is_write_query_with_complex_query():
    query = """
    MATCH (n:Person)
    WHERE n.age > 30
    WITH n
    CREATE (m:Message {text: 'Hello'})
    MERGE (n)-[:SENT]->(m)
    RETURN n, m
    """
    assert is_write_query(query)
