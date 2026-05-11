---
title: "Database Testing Strategies for Developers"
description: "Database testing with in-memory DBs for unit tests, Testcontainers for integration tests, migration testing, and property-based testing."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-testing.html
---

Database testing is often the weakest part of a test suite. Developers mock the database entirely and miss critical issues that only surface in production. This article covers practical database testing strategies: unit tests with in-memory databases, integration tests with Testcontainers, migration testing, data seeding, and property-based testing.

## The Database Testing Pyramid

Just as the test pyramid guides general testing strategy, database testing has its own levels:

```
         /\
        /  \        Property-based tests (few, high value)
       /    \
      /      \      Integration tests with real DB
     /        \
    /          \    Migration and seed tests
   /            \
  /              \  Unit tests with mocked/lightweight DB
 /________________\
```

Most teams over-invest in unit tests and under-invest in integration tests. For database testing, the opposite is true: the highest-value tests are those that use a real database.

## Unit Tests with In-Memory Databases

In-memory databases (H2, SQLite) are useful for testing your data access layer logic without setting up a full database server.

### When to Use In-Memory Databases

- Testing SQL query logic that does not rely on database-specific features.
- Testing repository methods and data access objects.
- Fast feedback during development.
- CI environments where a real database is not available.

### Limitations

In-memory databases are not perfect substitutes. They have different behavior in areas like:
- SQL dialect differences (H2's SQL differs from PostgreSQL's).
- Transaction isolation levels.
- Constraint enforcement.
- Type handling and precision.
- Performance characteristics.

```java
// Java: Unit test with H2 in-memory database
@ExtendWith(SpringExtension.class)
@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.ANY)
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldFindUserByEmail() {
        User saved = userRepository.save(
            new User("alice@example.com", "Alice")
        );
        
        User found = userRepository.findByEmail("alice@example.com");
        
        assertThat(found).isNotNull();
        assertThat(found.getName()).isEqualTo("Alice");
    }
}
```

```python
# Python: Unit test with SQLite in-memory
import pytest
import sqlite3
from myapp.repository import UserRepository

@pytest.fixture
def repo():
    conn = sqlite3.connect(':memory:')
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            name TEXT
        )
    """)
    return UserRepository(conn)

def test_find_by_email(repo):
    repo.create("alice@example.com", "Alice")
    user = repo.find_by_email("alice@example.com")
    assert user is not None
    assert user.name == "Alice"
```

## Integration Tests with Testcontainers

Testcontainers is a library that spins up disposable database containers for integration tests. It gives you a real database with the exact version you use in production.

### Why Testcontainers

- Tests run against the actual database engine (PostgreSQL, MySQL, etc.).
- No manual database setup or cleanup.
- Containers start quickly (seconds) and are isolated per test class.
- Supports database-specific features (PostgreSQL extensions, MySQL storage engines).

```java
// Java: Integration test with Testcontainers PostgreSQL
@Testcontainers
class OrderRepositoryTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private OrderRepository orderRepository;

    @Test
    void shouldCalculateTotalSalesForPeriod() {
        orderRepository.save(new Order("2026-01-01", 100.00));
        orderRepository.save(new Order("2026-01-02", 200.00));
        
        BigDecimal total = orderRepository.totalSalesBetween(
            LocalDate.of(2026, 1, 1),
            LocalDate.of(2026, 1, 31)
        );
        
        assertThat(total).isEqualByComparingTo("300.00");
    }
}
```

```python
# Python: Integration test with testcontainers
import pytest
from testcontainers.postgres import PostgresContainer
from myapp.repository import OrderRepository
from myapp.database import create_connection

@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:16") as pg:
        yield pg

@pytest.fixture
def repo(postgres_container):
    conn = create_connection(postgres_container.get_connection_url())
    # Run migrations
    conn.execute("""
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            order_date DATE,
            amount DECIMAL(10,2)
        )
    """)
    return OrderRepository(conn)

def test_total_sales(repo):
    repo.create("2026-01-01", 100.00)
    repo.create("2026-01-02", 200.00)
    
    total = repo.total_sales_between(
        "2026-01-01", "2026-01-31"
    )
    
    assert total == 300.00
```

### Testcontainers for Other Databases

```python
# Testcontainers for MongoDB
from testcontainers.mongodb import MongoDbContainer

def test_mongo_repository():
    with MongoDbContainer("mongo:7") as mongo:
        client = mongo.get_connection_client()
        # Test code here

# Testcontainers for MySQL
from testcontainers.mysql import MySqlContainer

def test_mysql_repository():
    with MySqlContainer("mysql:8") as mysql:
        connection_url = mysql.get_connection_url()
        # Test code here
```

## Migration Testing

Database migrations are one of the riskiest operations in software development. A bad migration can cause downtime or data loss.

### Backward Compatibility Testing

Test that old code works after a migration:

```python
def test_migration_backward_compatible():
    """Verify V2 migration works with V1 code."""
    # Apply V1 schema
    apply_migration("V1__initial_schema.sql")
    
    # Write data with V1 code
    repo = UserRepository(conn)
    repo.create("alice@example.com", "Alice")
    
    # Apply V2 migration
    apply_migration("V2__add_user_preferences.sql")
    
    # V1 code can still read data
    user = repo.find_by_email("alice@example.com")
    assert user is not None  # V1 code still works!
```

### Rollback Testing

Test that migration rollback works:

```python
def test_migration_rollback():
    """Verify migration is reversible."""
    apply_migration("V1__initial_schema.sql")
    apply_migration("V2__add_user_preferences.sql")
    
    # Rollback V2
    rollback_migration("V2__add_user_preferences.sql")
    
    # Schema should be back to V1
    columns = get_table_columns("users")
    assert "preferences" not in columns  # Preference column removed
```

### Performance Regression Testing

Test that migrations do not degrade query performance:

```python
def test_migration_no_performance_regression():
    """Verify migration doesn't slow common queries."""
    apply_migration("V1__initial_schema.sql")
    insert_test_data(conn, 10000)
    
    time_v1 = measure_query_time("""
        SELECT * FROM users WHERE email LIKE '%example.com'
    """)
    
    apply_migration("V2__add_email_index.sql")
    
    time_v2 = measure_query_time("""
        SELECT * FROM users WHERE email LIKE '%example.com'
    """)
    
    # V2 should be at least as fast for this query
    assert time_v2 <= time_v1 * 1.1
```

## Data Seeding for Tests

Seeding test data requires balancing coverage with maintainability.

### Factory Approach

```python
# Data factory for test seeding
import factory
from myapp.models import User, Order

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker('name')
    status = "active"

class OrderFactory(factory.Factory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)
    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    status = "completed"

# Usage in tests
def test_order_summary():
    user = UserFactory()
    orders = OrderFactory.create_batch(5, user=user)
    
    summary = generate_order_summary(user.id)
    assert summary["total_orders"] == 5
```

### Test Data Isolation

Each test should have its own data set. Never share data between tests:

1. **Transaction rollback**: Run each test in a transaction and roll back at the end.
2. **Schema per test**: Create a fresh schema for each test class.
3. **Cleanup after**: Delete test data in teardown (slower, more complex).

## Property-Based Testing

Property-based testing generates random inputs to verify that database invariants hold. It is more thorough than writing individual test cases.

```python
# Property-based testing with Hypothesis
from hypothesis import given, strategies as st

@given(
    st.lists(
        st.fixed_dictionaries({
            'email': st.emails(),
            'name': st.text(min_size=1, max_size=100),
            'age': st.integers(min_value=0, max_value=150)
        }),
        min_size=1,
        max_size=100
    )
)
def test_user_id_uniqueness(users):
    """All created users should have unique IDs."""
    user_ids = []
    for user_data in users:
        user_id = repo.create(
            user_data['email'],
            user_data['name'],
            user_data['age']
        )
        user_ids.append(user_id)
    
    assert len(set(user_ids)) == len(user_ids)
```

```javascript
// Property-based testing with fast-check
const fc = require('fast-check');

describe('User repository', () => {
    it('should enforce unique email constraint', () => {
        fc.assert(
            fc.property(fc.uniqueArray(fc.email(), {minLength: 1}), (emails) => {
                // Create users
                for (const email of emails) {
                    repo.create({email, name: 'Test'});
                }
                // Try to create duplicate
                expect(() => repo.create({
                    email: emails[0],
                    name: 'Duplicate'
                })).toThrow();
            })
        );
    });
});
```

## Testing Anti-Patterns

- **Shared mutable state**: Tests that modify shared database state and depend on each other. Always isolate test data.
- **Testing the framework**: Testing that a database returns the rows you inserted tests the database, not your code.
- **Mocking everything**: Mocks hide real issues like constraint violations, transaction handling, and deadlocks.
- **Flaky tests**: Tests that fail intermittently due to timing, data ordering, or environment dependencies.

## Conclusion

Database testing requires a layered strategy. Use in-memory databases for fast unit tests of data access logic. Use Testcontainers for integration tests against the exact production database engine. Test migrations for backward compatibility, rollback, and performance. Use property-based testing to discover edge cases. The most valuable database test is one that uses a real database, tests a real query, and verifies a real constraint.
