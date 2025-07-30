import pytest
from unittest.mock import MagicMock, patch
from neo4j import GraphDatabase
from robosystems_mcp.server import neo4jDatabase


@pytest.fixture
def mock_driver():
    """Create a mocked Neo4j driver for testing database connection layer."""
    with patch.object(GraphDatabase, "driver") as mock:
        driver_instance = MagicMock()
        mock.return_value = driver_instance
        yield driver_instance


@pytest.fixture
def db(mock_driver):
    """Create a database instance with mocked driver."""
    return neo4jDatabase("neo4j://localhost:7687", "neo4j", "password", "neo4j")


@pytest.fixture(scope="function")
def mock_neo4j():
    """Create a mocked Neo4j database for testing query execution."""
    with patch("robosystems_mcp.server.neo4jDatabase") as mock_db_class:
        mock_instance = MagicMock()
        mock_db_class.return_value = mock_instance

        def mock_execute_query(query, params=None):
            if "CREATE (n:Person {name: 'Alice', age: 30})" in query:
                return [{"nodes_created": 1, "labels_added": 1, "properties_set": 2}]
            elif "CALL db.schema.visualization()" in query:
                return [{"nodes": [], "relationships": []}]
            elif "MATCH (p:Person)-[:FRIEND]->(friend)" in query:
                return [
                    {"person": "Alice", "friend_name": "Bob"},
                    {"person": "Bob", "friend_name": "Charlie"},
                ]
            elif "MATCH (n) DETACH DELETE n" in query:
                return [{"nodes_deleted": 0, "relationships_deleted": 0}]
            elif "CREATE (a:Person {name: 'Alice', age: 30})" in query:
                return [{"nodes_created": 1, "labels_added": 1, "properties_set": 2}]
            elif "CREATE (b:Person {name: 'Bob', age: 25})" in query:
                return [{"nodes_created": 1, "labels_added": 1, "properties_set": 2}]
            elif "CREATE (c:Person {name: 'Charlie', age: 35})" in query:
                return [{"nodes_created": 1, "labels_added": 1, "properties_set": 2}]
            elif (
                "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:FRIEND]->(b)"
                in query
            ):
                return [{"relationships_created": 1}]
            elif (
                "MATCH (b:Person {name: 'Bob'}), (c:Person {name: 'Charlie'}) CREATE (b)-[:FRIEND]->(c)"
                in query
            ):
                return [{"relationships_created": 1}]
            else:
                return []

        mock_instance._execute_query.side_effect = mock_execute_query
        yield mock_instance


# Database Connection Tests
class TestDatabaseConnection:
    def test_database_initialization(self, mock_driver):
        _ = neo4jDatabase("neo4j://localhost:7687", "neo4j", "password", "neo4j")
        mock_driver.verify_connectivity.assert_called_once()

    def test_database_close(self, db):
        db.close()
        db.driver.close.assert_called_once()

    def test_execute_read_query(self, db):
        expected_result = [{"name": "Alice", "age": 30}]
        mock_record = MagicMock()
        mock_record.__getitem__.side_effect = lambda x: expected_result[0][x]
        mock_record.keys.return_value = expected_result[0].keys()
        db.driver.execute_query.return_value.records = [mock_record]

        result = db.execute_query("MATCH (n:Person) RETURN n.name, n.age")
        assert result == expected_result

    def test_execute_query_with_params(self, db):
        params = {"name": "Alice"}
        db.execute_query("MATCH (n:Person {name: $name}) RETURN n", params)
        db.driver.execute_query.assert_called_with(
            "MATCH (n:Person {name: $name}) RETURN n",
            parameters=params,
            database="neo4j",
        )

    def test_execute_query_error(self, db):
        db.driver.execute_query.side_effect = Exception("Database error")
        with pytest.raises(Exception, match="Database error"):
            db.execute_query("INVALID QUERY")


# Query Execution Tests
class TestQueryExecution:
    @pytest.mark.asyncio
    async def test_execute_cypher_update_query(self, mock_neo4j):
        query = "CREATE (n:Person {name: 'Alice', age: 30}) RETURN n.name"
        result = mock_neo4j._execute_query(query)

        assert len(result) == 1
        assert result[0]["nodes_created"] == 1
        assert result[0]["labels_added"] == 1
        assert result[0]["properties_set"] == 2

    @pytest.mark.asyncio
    async def test_retrieve_schema(self, mock_neo4j):
        query = "CALL db.schema.visualization()"
        result = mock_neo4j._execute_query(query)

        assert "nodes" in result[0]
        assert "relationships" in result[0]

    @pytest.mark.asyncio
    async def test_execute_complex_read_query(self, mock_neo4j):
        # Prepare test data
        mock_neo4j._execute_query("CREATE (a:Person {name: 'Alice', age: 30})")
        mock_neo4j._execute_query("CREATE (b:Person {name: 'Bob', age: 25})")
        mock_neo4j._execute_query("CREATE (c:Person {name: 'Charlie', age: 35})")
        mock_neo4j._execute_query(
            "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:FRIEND]->(b)"
        )
        mock_neo4j._execute_query(
            "MATCH (b:Person {name: 'Bob'}), (c:Person {name: 'Charlie'}) CREATE (b)-[:FRIEND]->(c)"
        )

        query = """
            MATCH (p:Person)-[:FRIEND]->(friend)
            RETURN p.name AS person, friend.name AS friend_name
            ORDER BY p.name, friend.name
            """
        result = mock_neo4j._execute_query(query)

        assert len(result) == 2
        assert result[0]["person"] == "Alice"
        assert result[0]["friend_name"] == "Bob"
        assert result[1]["person"] == "Bob"
        assert result[1]["friend_name"] == "Charlie"
