"""
Test the examples from README to ensure they work as documented
"""

import pytest
from ephemeraldb import EphemeralDB


class TestREADMEExamples:
    """Test all examples from the README"""
    
    def test_basic_usage_example(self):
        """Test the basic usage example from README"""
        # Create a new database instance
        db = EphemeralDB()

        # Basic usage
        db.set('name', 'Alice')
        db.set('user.age', 30)
        assert db.get('name') == 'Alice'
        assert db.get('user.age') == 30
    
    def test_scoped_usage_example(self):
        """Test the scoped usage example from README"""
        db = EphemeralDB()
        
        # Scoped usage
        db.set('global_var', 'I am global')

        db.push_scope('scope1')
        db.set('local_var', 'I am local')
        assert db.get('global_var') == 'I am global'  # accessible from parent
        assert db.get('local_var') == 'I am local'

        db.pop_scope()
        assert db.get('local_var') is None  # scope popped
    
    def test_context_manager_example(self):
        """Test the context manager example from README"""
        db = EphemeralDB()
        
        # Context manager usage
        with db.scope('temp_scope'):
            db.set('temp_data', 'temporary')
            assert db.get('temp_data') == 'temporary'
        
        # temp_data is automatically cleaned up
        assert db.get('temp_data') is None
    
    def test_dsl_interpreter_usecase(self):
        """Test a DSL interpreter use case"""
        db = EphemeralDB()
        
        # Simulate DSL interpreter with variable scoping
        def execute_block(variables, statements):
            """Simulate executing a block of statements with local variables"""
            with db.scope('block_scope'):
                # Import block variables
                for var, value in variables.items():
                    db.set(var, value)
                
                results = []
                for statement in statements:
                    if statement.startswith('SET '):
                        _, var, value = statement.split(' ', 2)
                        db.set(var, value)
                    elif statement.startswith('GET '):
                        _, var = statement.split(' ', 1)
                        results.append(db.get(var))
                
                return results
        
        # Set global variables
        db.set('global_constant', 42)
        
        # Execute nested blocks
        results1 = execute_block(
            {'local_var': 'block1'},
            ['SET temp_var hello', 'GET local_var', 'GET temp_var', 'GET global_constant']
        )
        
        assert results1 == ['block1', 'hello', 42]
        
        # Variables should be cleaned up
        assert db.get('local_var') is None
        assert db.get('temp_var') is None
        assert db.get('global_constant') == 42
    
    def test_configuration_parser_usecase(self):
        """Test a configuration parser use case"""
        db = EphemeralDB()
        
        def parse_config_section(section_name, config_data):
            """Parse a configuration section with inheritance"""
            with db.scope(f'config_{section_name}'):
                for key, value in config_data.items():
                    db.set(f'{section_name}.{key}', value)
                
                # Return resolved configuration
                return {
                    'section': section_name,
                    'resolved_config': db.to_dict(include_hierarchy=True)
                }
        
        # Set global defaults
        db.set('defaults.timeout', 30)
        db.set('defaults.retries', 3)
        
        # Parse environment-specific configs
        dev_config = parse_config_section('development', {
            'host': 'localhost',
            'port': 8000,
            'debug': True
        })
        
        prod_config = parse_config_section('production', {
            'host': 'prod.example.com',
            'port': 443,
            'timeout': 60  # Override default
        })
        
        # Verify inheritance works
        assert dev_config['resolved_config']['defaults.timeout'] == 30
        assert dev_config['resolved_config']['development.debug'] is True
        
        assert prod_config['resolved_config']['defaults.retries'] == 3
        assert prod_config['resolved_config']['production.timeout'] == 60
    
    def test_nested_transaction_usecase(self):
        """Test nested transaction processing use case"""
        db = EphemeralDB()
        
        class Transaction:
            def __init__(self, db, name):
                self.db = db
                self.name = name
                self.changes = []
            
            def __enter__(self):
                self.db.push_scope(f'transaction_{self.name}')
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    # Transaction succeeded, record changes
                    self.changes = list(self.db.items(include_nested=False))
                else:
                    # Transaction failed, changes will be rolled back automatically
                    pass
                self.db.pop_scope()
        
        # Set initial state
        db.set('account.balance', 1000)
        db.set('account.transactions', [])
        
        # Nested transactions
        try:
            with Transaction(db, 'outer') as outer_tx:
                db.set('pending.amount', 200)
                
                with Transaction(db, 'inner') as inner_tx:
                    current_balance = db.get('account.balance')
                    pending_amount = db.get('pending.amount')
                    
                    if current_balance >= pending_amount:
                        db.set('account.balance', current_balance - pending_amount)
                        db.set('temp.new_balance', current_balance - pending_amount)
                    else:
                        raise ValueError("Insufficient funds")
                
                # Inner transaction succeeded
                new_balance = db.get('temp.new_balance')
                if new_balance is not None:
                    db.set('account.balance', new_balance)
        
        except ValueError:
            # Transaction rolled back
            pass
        
        # Verify final state
        assert db.get('account.balance') == 1000  # Transaction was rolled back due to scope cleanup
        assert db.get('pending.amount') is None  # Cleaned up
        assert db.get('temp.new_balance') is None  # Cleaned up


class TestAdvancedUseCases:
    """Test advanced use cases and patterns"""
    
    def test_template_engine_context(self):
        """Test template engine variable context management"""
        db = EphemeralDB()
        
        def render_template(template, context):
            """Simulate template rendering with variable context"""
            with db.scope('template_context'):
                # Set template variables
                for key, value in context.items():
                    db.set(key, value)
                
                # Simple template variable substitution
                result = template
                # Get all keys from current scope and parent scopes
                all_keys = set()
                for scope in reversed(db._scopes):
                    for key in scope.keys():
                        if '.' not in key:  # Only top-level variables
                            all_keys.add(key)
                
                for key in all_keys:
                    value = db.get(key)
                    if value is not None:
                        result = result.replace(f'{{{key}}}', str(value))
                
                return result
        
        # Set global template variables
        db.set('site_name', 'My Website')
        db.set('copyright_year', 2024)
        
        # Render templates with local context
        template1 = "Welcome to {site_name}! Hello {user_name}!"
        result1 = render_template(template1, {'user_name': 'Alice'})
        assert result1 == "Welcome to My Website! Hello Alice!"
        
        template2 = "© {copyright_year} {site_name}. User: {user_name}"
        result2 = render_template(template2, {'user_name': 'Bob'})
        assert result2 == "© 2024 My Website. User: Bob"
        
        # Verify isolation
        assert db.get('user_name') is None
    
    def test_recursive_function_context(self):
        """Test recursive function with context preservation"""
        db = EphemeralDB()
        
        def recursive_processor(data, depth=0):
            """Process nested data with depth-aware context"""
            with db.scope(f'depth_{depth}'):
                db.set('current_depth', depth)
                
                # Update max_depth in root scope, not current scope
                current_max = db.get('max_depth', 0)
                if depth > current_max:
                    # Set max_depth in root scope
                    if len(db._scopes) > 1:
                        db._scopes[0]['max_depth'] = depth
                    else:
                        db.set('max_depth', depth)
                
                if isinstance(data, dict):
                    result = {}
                    for key, value in data.items():
                        db.set(f'processing_key', key)
                        result[key] = recursive_processor(value, depth + 1)
                    return result
                elif isinstance(data, list):
                    result = []
                    for i, item in enumerate(data):
                        db.set(f'processing_index', i)
                        result.append(recursive_processor(item, depth + 1))
                    return result
                else:
                    # Leaf node - add depth info
                    current_depth = db.get('current_depth')
                    return f"{data}_depth{current_depth}"
        
        # Test with nested structure
        test_data = {
            'level1': {
                'level2': {
                    'level3': 'deep_value'
                },
                'list': [1, 2, {'nested_in_list': 'value'}]
            },
            'simple': 'simple_value'
        }
        
        result = recursive_processor(test_data)
        
        # Verify processing worked correctly
        assert result['level1']['level2']['level3'] == 'deep_value_depth3'
        assert result['level1']['list'][0] == '1_depth3'  # Items in list are processed at depth 3
        assert result['level1']['list'][2]['nested_in_list'] == 'value_depth4'  # Nested in list at depth 4
        assert result['simple'] == 'simple_value_depth1'
        
        # Verify context was cleaned up
        assert db.get('current_depth') is None
        assert db.get('processing_key') is None
        assert db.get('max_depth') == 4  # This should persist as it was set in root scope (depth 4 for nested_in_list)