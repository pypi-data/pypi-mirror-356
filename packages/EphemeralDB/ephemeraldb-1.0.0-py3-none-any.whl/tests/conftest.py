"""
Pytest configuration and fixtures for EphemeralDB tests
"""

import pytest
from ephemeraldb import EphemeralDB


@pytest.fixture
def db():
    """Provide a fresh EphemeralDB instance for each test"""
    return EphemeralDB()


@pytest.fixture
def populated_db():
    """Provide an EphemeralDB instance with some test data"""
    db = EphemeralDB()
    
    # Add some test data
    db.set('string_key', 'string_value')
    db.set('int_key', 42)
    db.set('list_key', [1, 2, 3])
    db.set('dict_key', {'nested': 'value'})
    db.set('nested.key1', 'nested_value1')
    db.set('nested.key2', 'nested_value2')
    db.set('deep.nested.key', 'deep_value')
    
    return db


@pytest.fixture
def multi_scope_db():
    """Provide an EphemeralDB instance with multiple scopes set up"""
    db = EphemeralDB()
    
    # Root scope data
    db.set('global_var', 'global_value')
    db.set('shared_key', 'root_value')
    
    # Level 1 scope
    db.push_scope('level1')
    db.set('level1_var', 'level1_value')
    db.set('shared_key', 'level1_value')  # Shadow root value
    
    # Level 2 scope
    db.push_scope('level2')
    db.set('level2_var', 'level2_value')
    
    return db