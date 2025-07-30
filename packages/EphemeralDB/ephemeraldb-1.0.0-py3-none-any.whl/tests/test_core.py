"""
Tests for EphemeralDB core functionality
"""

import pytest
import threading
import time
from unittest.mock import patch

from ephemeraldb import EphemeralDB
from ephemeraldb.exceptions import ScopeError, KeyError as EphemeralKeyError


class TestBasicOperations:
    """Test basic CRUD operations"""
    
    def test_set_and_get(self):
        """Test basic set and get operations"""
        db = EphemeralDB()
        
        db.set('key1', 'value1')
        assert db.get('key1') == 'value1'
        
        db.set('key2', 42)
        assert db.get('key2') == 42
        
        db.set('key3', [1, 2, 3])
        assert db.get('key3') == [1, 2, 3]
    
    def test_get_default_value(self):
        """Test get with default values"""
        db = EphemeralDB()
        
        assert db.get('nonexistent') is None
        assert db.get('nonexistent', 'default') == 'default'
        assert db.get('nonexistent', 42) == 42
    
    def test_delete(self):
        """Test delete operations"""
        db = EphemeralDB()
        
        db.set('key1', 'value1')
        assert db.exists('key1')
        
        result = db.delete('key1')
        assert result is True
        assert not db.exists('key1')
        
        # Delete non-existent key
        result = db.delete('nonexistent')
        assert result is False
    
    def test_exists(self):
        """Test exists operations"""
        db = EphemeralDB()
        
        assert not db.exists('key1')
        
        db.set('key1', 'value1')
        assert db.exists('key1')
        
        db.delete('key1')
        assert not db.exists('key1')
    
    def test_clear(self):
        """Test clear operation"""
        db = EphemeralDB()
        
        db.set('key1', 'value1')
        db.set('key2', 'value2')
        
        assert db.exists('key1')
        assert db.exists('key2')
        
        db.clear()
        
        assert not db.exists('key1')
        assert not db.exists('key2')


class TestNestedKeys:
    """Test dot notation and nested key functionality"""
    
    def test_nested_key_operations(self):
        """Test nested key operations with dot notation"""
        db = EphemeralDB()
        
        db.set('user.name', 'Alice')
        db.set('user.profile.age', 30)
        db.set('user.profile.email', 'alice@example.com')
        
        assert db.get('user.name') == 'Alice'
        assert db.get('user.profile.age') == 30
        assert db.get('user.profile.email') == 'alice@example.com'
    
    def test_nested_key_overwrite(self):
        """Test overwriting nested structures"""
        db = EphemeralDB()
        
        db.set('config.database.host', 'localhost')
        db.set('config.database.port', 5432)
        
        # Overwrite entire database config
        db.set('config.database', 'sqlite:///test.db')
        
        assert db.get('config.database') == 'sqlite:///test.db'
        assert db.get('config.database.host') is None
    
    def test_nested_key_delete(self):
        """Test deleting nested keys"""
        db = EphemeralDB()
        
        db.set('app.settings.debug', True)
        db.set('app.settings.port', 8000)
        db.set('app.name', 'MyApp')
        
        # Delete specific nested key
        result = db.delete('app.settings.debug')
        assert result is True
        assert db.get('app.settings.debug') is None
        assert db.get('app.settings.port') == 8000
        assert db.get('app.name') == 'MyApp'
    
    def test_nested_key_exists(self):
        """Test exists with nested keys"""
        db = EphemeralDB()
        
        db.set('level1.level2.level3', 'deep_value')
        
        assert db.exists('level1.level2.level3')
        assert not db.exists('level1.level2.level4')
        assert not db.exists('level1.nonexistent')


class TestScopeManagement:
    """Test scope push/pop functionality"""
    
    def test_basic_scope_operations(self):
        """Test basic scope push and pop"""
        db = EphemeralDB()
        
        # Initially has root scope
        assert db.scope_count() == 1
        assert db.current_scope() is None
        
        # Push a scope
        db.push_scope('scope1')
        assert db.scope_count() == 2
        assert db.current_scope() == 'scope1'
        
        # Pop the scope
        popped_data = db.pop_scope()
        assert db.scope_count() == 1
        assert db.current_scope() is None
        assert isinstance(popped_data, dict)
    
    def test_scope_data_isolation(self):
        """Test that scope data is properly isolated"""
        db = EphemeralDB()
        
        # Set data in root scope
        db.set('global_var', 'global_value')
        
        # Push scope and set local data
        db.push_scope('local_scope')
        db.set('local_var', 'local_value')
        
        # Both should be accessible
        assert db.get('global_var') == 'global_value'
        assert db.get('local_var') == 'local_value'
        
        # Pop scope
        db.pop_scope()
        
        # Only global should be accessible
        assert db.get('global_var') == 'global_value'
        assert db.get('local_var') is None
    
    def test_nested_scopes(self):
        """Test multiple nested scopes"""
        db = EphemeralDB()
        
        db.set('level0', 'root')
        
        db.push_scope('level1')
        db.set('level1_var', 'level1_value')
        
        db.push_scope('level2')
        db.set('level2_var', 'level2_value')
        
        # All levels should be accessible
        assert db.get('level0') == 'root'
        assert db.get('level1_var') == 'level1_value'
        assert db.get('level2_var') == 'level2_value'
        assert db.scope_count() == 3
        
        # Pop one level
        db.pop_scope()
        assert db.get('level0') == 'root'
        assert db.get('level1_var') == 'level1_value'
        assert db.get('level2_var') is None
        assert db.scope_count() == 2
        
        # Pop another level
        db.pop_scope()
        assert db.get('level0') == 'root'
        assert db.get('level1_var') is None
        assert db.scope_count() == 1
    
    def test_cannot_pop_root_scope(self):
        """Test that root scope cannot be popped"""
        db = EphemeralDB()
        
        with pytest.raises(ScopeError, match="ルートスコープを削除できません"):
            db.pop_scope()
    
    def test_scope_shadowing(self):
        """Test that child scopes can shadow parent scope values"""
        db = EphemeralDB()
        
        db.set('shared_key', 'parent_value')
        
        db.push_scope('child')
        db.set('shared_key', 'child_value')
        
        # Child value should be returned
        assert db.get('shared_key') == 'child_value'
        
        db.pop_scope()
        
        # Parent value should be restored
        assert db.get('shared_key') == 'parent_value'


class TestContextManager:
    """Test context manager functionality"""
    
    def test_context_manager_basic(self):
        """Test basic context manager usage"""
        db = EphemeralDB()
        
        db.set('global_var', 'global')
        
        with db.scope('temp_scope'):
            assert db.current_scope() == 'temp_scope'
            db.set('temp_var', 'temporary')
            assert db.get('temp_var') == 'temporary'
            assert db.get('global_var') == 'global'
        
        # After context exit
        assert db.current_scope() is None
        assert db.get('temp_var') is None
        assert db.get('global_var') == 'global'
    
    def test_context_manager_exception(self):
        """Test context manager cleanup on exception"""
        db = EphemeralDB()
        
        initial_count = db.scope_count()
        
        try:
            with db.scope('error_scope'):
                db.set('temp_data', 'will_be_lost')
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Scope should be cleaned up even after exception
        assert db.scope_count() == initial_count
        assert db.get('temp_data') is None
    
    def test_nested_context_managers(self):
        """Test nested context managers"""
        db = EphemeralDB()
        
        db.set('level0', 'root')
        
        with db.scope('level1'):
            db.set('level1_var', 'level1')
            
            with db.scope('level2'):
                db.set('level2_var', 'level2')
                
                assert db.get('level0') == 'root'
                assert db.get('level1_var') == 'level1'
                assert db.get('level2_var') == 'level2'
                assert db.scope_count() == 3
            
            # After inner context
            assert db.get('level2_var') is None
            assert db.get('level1_var') == 'level1'
            assert db.scope_count() == 2
        
        # After outer context
        assert db.get('level1_var') is None
        assert db.scope_count() == 1


class TestUtilityMethods:
    """Test utility and introspection methods"""
    
    def test_keys_method(self):
        """Test keys() method"""
        db = EphemeralDB()
        
        db.set('simple_key', 'value')
        db.set('nested.key', 'nested_value')
        db.set('deeply.nested.key', 'deep_value')
        
        keys = db.keys()
        assert 'simple_key' in keys
        assert 'nested.key' in keys
        assert 'deeply.nested.key' in keys
        
        # Test without nested keys
        keys_flat = db.keys(include_nested=False)
        assert 'simple_key' in keys_flat
        assert 'nested' in keys_flat
        assert 'deeply' in keys_flat
        assert 'nested.key' not in keys_flat
    
    def test_items_method(self):
        """Test items() method"""
        db = EphemeralDB()
        
        db.set('key1', 'value1')
        db.set('nested.key2', 'value2')
        
        items = db.items()
        
        # Should include nested items as flattened
        items_dict = dict(items)
        assert items_dict['key1'] == 'value1'
        assert items_dict['nested.key2'] == 'value2'
    
    def test_to_dict_method(self):
        """Test to_dict() method"""
        db = EphemeralDB()
        
        db.set('root_key', 'root_value')
        
        db.push_scope('child')
        db.set('child_key', 'child_value')
        
        # Current scope only
        current_dict = db.to_dict()
        assert 'child_key' in current_dict
        assert 'root_key' not in current_dict
        
        # Include hierarchy
        full_dict = db.to_dict(include_hierarchy=True)
        assert 'child_key' in full_dict
        assert 'root_key' in full_dict
    
    def test_from_dict_method(self):
        """Test from_dict() method"""
        db = EphemeralDB()
        
        data = {
            'key1': 'value1',
            'key2': 42,
            'nested': {'inner': 'inner_value'}
        }
        
        db.from_dict(data)
        
        assert db.get('key1') == 'value1'
        assert db.get('key2') == 42
        assert db.get('nested') == {'inner': 'inner_value'}
    
    def test_len_and_contains(self):
        """Test __len__ and __contains__ methods"""
        db = EphemeralDB()
        
        assert len(db) == 0
        
        db.set('key1', 'value1')
        db.set('nested.key2', 'value2')
        
        # len() counts leaf keys only (not intermediate dictionary nodes)
        assert len(db) == 2
        assert 'key1' in db
        assert 'nested.key2' in db
        assert 'nonexistent' not in db
    
    def test_repr(self):
        """Test __repr__ method"""
        db = EphemeralDB()
        
        repr_str = repr(db)
        assert 'EphemeralDB' in repr_str
        assert 'scopes=1' in repr_str
        
        db.push_scope('named_scope')
        repr_str = repr(db)
        assert 'scopes=2' in repr_str
        assert "current='named_scope'" in repr_str


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_key_type(self):
        """Test handling of invalid key types"""
        db = EphemeralDB()
        
        with pytest.raises(EphemeralKeyError):
            db.set(123, 'value')
        
        with pytest.raises(EphemeralKeyError):
            db.get(None)
        
        with pytest.raises(EphemeralKeyError):
            db.delete([1, 2, 3])
    
    def test_empty_key(self):
        """Test handling of empty keys"""
        db = EphemeralDB()
        
        # Empty string should raise an error now
        with pytest.raises(EphemeralKeyError, match="キーは空文字列にできません"):
            db.set('', 'empty_key_value')
    
    def test_complex_nested_structures(self):
        """Test complex nested data structures"""
        db = EphemeralDB()
        
        complex_data = {
            'users': [
                {'name': 'Alice', 'age': 30},
                {'name': 'Bob', 'age': 25}
            ],
            'config': {
                'database': {
                    'host': 'localhost',
                    'port': 5432,
                    'credentials': {
                        'username': 'admin',
                        'password': 'secret'
                    }
                }
            }
        }
        
        db.set('app_data', complex_data)
        retrieved_data = db.get('app_data')
        
        assert retrieved_data == complex_data
        assert retrieved_data['users'][0]['name'] == 'Alice'
        assert retrieved_data['config']['database']['credentials']['username'] == 'admin'


class TestThreadSafety:
    """Test thread safety"""
    
    def test_concurrent_operations(self):
        """Test concurrent read/write operations"""
        db = EphemeralDB()
        results = []
        errors = []
        
        def worker(worker_id):
            try:
                for i in range(100):
                    key = f'worker_{worker_id}_key_{i}'
                    value = f'worker_{worker_id}_value_{i}'
                    
                    db.set(key, value)
                    retrieved = db.get(key)
                    
                    if retrieved == value:
                        results.append(f'{worker_id}_{i}_success')
                    else:
                        errors.append(f'{worker_id}_{i}_mismatch')
                    
                    time.sleep(0.001)  # Small delay to increase chance of race conditions
            except Exception as e:
                errors.append(f'{worker_id}_exception_{str(e)}')
        
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 500  # 5 workers * 100 operations each
    
    def test_concurrent_scope_operations(self):
        """Test concurrent scope operations"""
        db = EphemeralDB()
        db.set('global_key', 'global_value')
        
        results = []
        errors = []
        
        def scope_worker(worker_id):
            try:
                with db.scope(f'worker_{worker_id}'):
                    db.set(f'local_key_{worker_id}', f'local_value_{worker_id}')
                    
                    # Verify we can see global data
                    global_val = db.get('global_key')
                    if global_val == 'global_value':
                        results.append(f'{worker_id}_global_success')
                    
                    # Verify we can see our local data
                    local_val = db.get(f'local_key_{worker_id}')
                    if local_val == f'local_value_{worker_id}':
                        results.append(f'{worker_id}_local_success')
                    
                    time.sleep(0.01)
            except Exception as e:
                errors.append(f'{worker_id}_exception_{str(e)}')
        
        threads = []
        for i in range(10):
            thread = threading.Thread(target=scope_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 20  # 10 workers * 2 success checks each
        
        # Verify all scopes were cleaned up
        assert db.scope_count() == 1


class TestPerformance:
    """Basic performance tests"""
    
    def test_large_dataset_operations(self):
        """Test operations with large datasets"""
        db = EphemeralDB()
        
        # Set many keys
        start_time = time.time()
        for i in range(1000):
            db.set(f'key_{i}', f'value_{i}')
        set_time = time.time() - start_time
        
        # Get many keys
        start_time = time.time()
        for i in range(1000):
            value = db.get(f'key_{i}')
            assert value == f'value_{i}'
        get_time = time.time() - start_time
        
        # Basic performance assertions (should be fast)
        assert set_time < 1.0, f"Set operations took too long: {set_time}s"
        assert get_time < 1.0, f"Get operations took too long: {get_time}s"
    
    def test_deep_nesting_performance(self):
        """Test performance with deeply nested keys"""
        db = EphemeralDB()
        
        # Create deeply nested structure
        deep_key = '.'.join([f'level_{i}' for i in range(20)])
        
        start_time = time.time()
        db.set(deep_key, 'deep_value')
        set_time = time.time() - start_time
        
        start_time = time.time()
        value = db.get(deep_key)
        get_time = time.time() - start_time
        
        assert value == 'deep_value'
        assert set_time < 0.1, f"Deep set took too long: {set_time}s"
        assert get_time < 0.1, f"Deep get took too long: {get_time}s"