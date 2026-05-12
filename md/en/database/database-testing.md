---
title: "Database Testing Strategies for Developers"
description: "Database testing with in-memory DBs for unit tests, Testcontainers for integration tests, migration testing, and property-based testing."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-testing.html
---

# Database Testing Strategies for Developers

Database Testing Strategies   
Database testing is often the weakest part of test suites. Effective strategies catch issues before production.   
Unit Tests with In-Memory DB   
In-memory databases provide fast feedback during development:   

    
    
    @pytest.fixture
    
    def repo():
    
        conn = sqlite3.connect(':memory:')
    
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT)")
    
        return UserRepository(conn)
    
    
    
    def test_find_by_email(repo):
    
        repo.create("alice@example.com", "Alice")
    
        user = repo.find_by_email("alice@example.com")
    
        assert user is not None
    
    

  
Integration Tests with Testcontainers   
Testcontainers spins up disposable database containers:   

    
    
    @pytest.fixture(scope="module")
    
    def postgres():
    
        with PostgresContainer("postgres:16") as pg:
    
            yield pg
    
    
    
    def test_order_total(repo):
    
        repo.create("2026-01-01", 100.00)
    
        total = repo.total_sales_between("2026-01-01", "2026-01-31")
    
        assert total == 100.00
    
    

  
Migration Testing   
Test that migrations are backward-compatible and rollbacks work:   

    
    
    def test_rollback():
    
        apply_migration("V1__initial.sql")
    
        apply_migration("V2__add_column.sql")
    
        rollback_migration("V2__add_column.sql")
    
        columns = get_table_columns("users")
    
        assert "new_column" not in columns
    
    

  
Data Fixtures   
Use factory patterns for test data:   

    
    
    class UserFactory:
    
        email = factory.Sequence(lambda n: f"user{n}@example.com")
    
        name = factory.Faker('name')
    
    

  
Conclusion   
Use in-memory databases for fast unit tests. Use Testcontainers for integration tests against real databases. Test migrations for backward compatibility. Use factory patterns for data fixtures. The most valuable test is one that uses a real database.
