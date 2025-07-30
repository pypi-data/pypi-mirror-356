"""
Core implementation of EphemeralDB
"""

import threading
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Iterator, Tuple
from collections import defaultdict

from .exceptions import ScopeError, KeyError as EphemeralKeyError, ValidationError, CapacityError


class EphemeralDB:
    """
    A lightweight volatile context management store with scoped key-value storage.
    
    Features:
    - Hierarchical scoping with push/pop operations
    - Dot notation support for nested keys
    - Thread-safe operations
    - Context manager support
    - Parent scope data inheritance
    """
    
    def __init__(self, max_scopes: int = 1000, max_keys_per_scope: int = 10000):
        """
        Initialize EphemeralDB with a root scope.
        
        Args:
            max_scopes: Maximum number of scopes allowed (default: 1000)
            max_keys_per_scope: Maximum number of keys per scope (default: 10000)
        """
        if max_scopes < 1:
            raise ValidationError("max_scopes must be at least 1", "INVALID_MAX_SCOPES")
        if max_keys_per_scope < 1:
            raise ValidationError("max_keys_per_scope must be at least 1", "INVALID_MAX_KEYS")
        
        self._lock = threading.RLock()
        self._scopes: List[Dict[str, Any]] = [{}]  # Stack of scopes, root scope at index 0
        self._scope_names: List[Optional[str]] = [None]  # Names of scopes
        self._max_scopes = max_scopes
        self._max_keys_per_scope = max_keys_per_scope
    
    def _parse_key(self, key: str) -> List[str]:
        """Parse a dot-separated key into components."""
        if not isinstance(key, str):
            raise EphemeralKeyError(
                f"キーは文字列である必要があります。{type(key).__name__}型が指定されました", 
                "INVALID_KEY_TYPE",
                {"provided_type": type(key).__name__, "expected_type": "str"}
            )
        
        if not key:
            raise EphemeralKeyError("キーは空文字列にできません", "EMPTY_KEY")
        
        if len(key) > 1000:  # Reasonable limit for key length
            raise EphemeralKeyError(
                f"キーが長すぎます（最大1000文字）: {len(key)}文字", 
                "KEY_TOO_LONG",
                {"key_length": len(key), "max_length": 1000}
            )
        
        return key.split('.')
    
    def _check_capacity_limits(self, scope_index: int = -1) -> None:
        """Check if capacity limits are exceeded."""
        current_scope = self._scopes[scope_index]
        key_count = len(self.keys())
        
        if key_count >= self._max_keys_per_scope:
            raise CapacityError(
                f"スコープ内のキー数が上限を超えました: {key_count}/{self._max_keys_per_scope}",
                "MAX_KEYS_EXCEEDED",
                {"current_keys": key_count, "max_keys": self._max_keys_per_scope}
            )
    
    def _get_nested_value(self, data: Dict[str, Any], key_parts: List[str]) -> Any:
        """Get a nested value from a dictionary using key parts."""
        current = data
        for part in key_parts:
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]
        return current
    
    def _set_nested_value(self, data: Dict[str, Any], key_parts: List[str], value: Any) -> None:
        """Set a nested value in a dictionary using key parts."""
        current = data
        for part in key_parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[key_parts[-1]] = value
    
    def _delete_nested_value(self, data: Dict[str, Any], key_parts: List[str]) -> bool:
        """Delete a nested value from a dictionary using key parts."""
        if len(key_parts) == 1:
            if key_parts[0] in data:
                del data[key_parts[0]]
                return True
            return False
        
        current = data
        for part in key_parts[:-1]:
            if not isinstance(current, dict) or part not in current:
                return False
            current = current[part]
        
        if isinstance(current, dict) and key_parts[-1] in current:
            del current[key_parts[-1]]
            return True
        return False
    
    def set(self, key: str, value: Any) -> None:
        """
        Store a value in the current scope.
        
        Args:
            key: The key to store the value under (supports dot notation)
            value: The value to store
            
        Raises:
            EphemeralKeyError: If key is invalid
            CapacityError: If capacity limits are exceeded
        """
        with self._lock:
            key_parts = self._parse_key(key)
            
            # Check capacity before adding
            self._check_capacity_limits()
            
            current_scope = self._scopes[-1]
            self._set_nested_value(current_scope, key_parts, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from the current scope or parent scopes.
        
        Args:
            key: The key to retrieve (supports dot notation)
            default: Default value if key is not found
            
        Returns:
            The stored value or default
        """
        with self._lock:
            key_parts = self._parse_key(key)
            
            # Search from current scope up to root scope
            for scope in reversed(self._scopes):
                value = self._get_nested_value(scope, key_parts)
                if value is not None:
                    return value
            
            return default
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the current scope.
        
        Args:
            key: The key to delete (supports dot notation)
            
        Returns:
            True if key was deleted, False if key was not found
        """
        with self._lock:
            key_parts = self._parse_key(key)
            current_scope = self._scopes[-1]
            return self._delete_nested_value(current_scope, key_parts)
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in current scope or parent scopes.
        
        Args:
            key: The key to check (supports dot notation)
            
        Returns:
            True if key exists, False otherwise
        """
        with self._lock:
            key_parts = self._parse_key(key)
            
            # Search from current scope up to root scope
            for scope in reversed(self._scopes):
                value = self._get_nested_value(scope, key_parts)
                if value is not None:
                    return True
            
            return False
    
    def clear(self) -> None:
        """Clear all data in the current scope."""
        with self._lock:
            self._scopes[-1].clear()
    
    def push_scope(self, name: Optional[str] = None) -> None:
        """
        Create a new scope and push it onto the stack.
        
        Args:
            name: Optional name for the scope
            
        Raises:
            CapacityError: If maximum number of scopes is exceeded
            ValidationError: If scope name is invalid
        """
        with self._lock:
            if len(self._scopes) >= self._max_scopes:
                raise CapacityError(
                    f"最大スコープ数を超えました: {len(self._scopes)}/{self._max_scopes}",
                    "MAX_SCOPES_EXCEEDED",
                    {"current_scopes": len(self._scopes), "max_scopes": self._max_scopes}
                )
            
            if name is not None:
                if not isinstance(name, str):
                    raise ValidationError(
                        f"スコープ名は文字列である必要があります: {type(name).__name__}型が指定されました",
                        "INVALID_SCOPE_NAME_TYPE",
                        {"provided_type": type(name).__name__}
                    )
                
                if len(name) > 100:  # Reasonable limit
                    raise ValidationError(
                        f"スコープ名が長すぎます（最大100文字）: {len(name)}文字",
                        "SCOPE_NAME_TOO_LONG",
                        {"name_length": len(name), "max_length": 100}
                    )
            
            self._scopes.append({})
            self._scope_names.append(name)
    
    def pop_scope(self) -> Dict[str, Any]:
        """
        Remove the current scope from the stack.
        
        Returns:
            The data from the popped scope
            
        Raises:
            ScopeError: If trying to pop the root scope
        """
        with self._lock:
            if len(self._scopes) <= 1:
                raise ScopeError(
                    "ルートスコープを削除できません",
                    "CANNOT_POP_ROOT_SCOPE",
                    {"current_scope_count": len(self._scopes)}
                )
            
            self._scope_names.pop()
            return self._scopes.pop()
    
    def current_scope(self) -> Optional[str]:
        """
        Get the name of the current scope.
        
        Returns:
            The name of the current scope or None if unnamed
        """
        with self._lock:
            return self._scope_names[-1]
    
    def scope_count(self) -> int:
        """
        Get the number of active scopes.
        
        Returns:
            The number of scopes (including root)
        """
        with self._lock:
            return len(self._scopes)
    
    @contextmanager
    def scope(self, name: Optional[str] = None) -> Iterator['EphemeralDB']:
        """
        Context manager for creating temporary scopes.
        
        Args:
            name: Optional name for the scope
            
        Yields:
            The EphemeralDB instance
        """
        self.push_scope(name)
        try:
            yield self
        finally:
            self.pop_scope()
    
    def keys(self, include_nested: bool = True) -> List[str]:
        """
        Get all keys in the current scope.
        
        Args:
            include_nested: If True, include nested keys with dot notation
            
        Returns:
            List of keys
        """
        with self._lock:
            current_scope = self._scopes[-1]
            
            if not include_nested:
                return list(current_scope.keys())
            
            keys = []
            
            def extract_keys(data: Dict[str, Any], prefix: str = ""):
                for key, value in data.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    
                    if isinstance(value, dict):
                        extract_keys(value, full_key)
                    else:
                        keys.append(full_key)
            
            extract_keys(current_scope)
            return keys
    
    def items(self, include_nested: bool = True) -> List[Tuple[str, Any]]:
        """
        Get all key-value pairs in the current scope.
        
        Args:
            include_nested: If True, include nested keys with dot notation
            
        Returns:
            List of (key, value) tuples
        """
        with self._lock:
            current_scope = self._scopes[-1]
            
            if not include_nested:
                return list(current_scope.items())
            
            items = []
            
            def extract_items(data: Dict[str, Any], prefix: str = ""):
                for key, value in data.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    
                    if isinstance(value, dict):
                        extract_items(value, full_key)
                    else:
                        items.append((full_key, value))
            
            extract_items(current_scope)
            return items
    
    def to_dict(self, include_hierarchy: bool = False) -> Dict[str, Any]:
        """
        Export current scope data as a dictionary.
        
        Args:
            include_hierarchy: If True, include data from parent scopes
            
        Returns:
            Dictionary containing the data
        """
        with self._lock:
            if not include_hierarchy:
                return dict(self._scopes[-1])
            
            # Merge all scopes from root to current, flattening nested keys
            merged = {}
            
            def flatten_dict(data: Dict[str, Any], prefix: str = ""):
                for key, value in data.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, dict):
                        flatten_dict(value, full_key)
                    else:
                        merged[full_key] = value
            
            for scope in self._scopes:
                flatten_dict(scope)
            
            return merged
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Import dictionary data into the current scope.
        
        Args:
            data: Dictionary to import
        """
        with self._lock:
            current_scope = self._scopes[-1]
            current_scope.update(data)
    
    def __repr__(self) -> str:
        """String representation of EphemeralDB."""
        with self._lock:
            scope_info = f"scopes={len(self._scopes)}"
            current_name = self.current_scope()
            if current_name:
                scope_info += f", current='{current_name}'"
            
            return f"EphemeralDB({scope_info})"
    
    def __len__(self) -> int:
        """Get the number of keys in the current scope."""
        with self._lock:
            return len(self.keys())
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists (supports 'in' operator)."""
        return self.exists(key)