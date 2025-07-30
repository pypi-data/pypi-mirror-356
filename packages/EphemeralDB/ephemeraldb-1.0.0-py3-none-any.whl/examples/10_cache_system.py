#!/usr/bin/env python3
"""
10. キャッシュシステム - 階層的キャッシュシステムの実装
"""

from ephemeraldb import EphemeralDB
import time
import hashlib
import json
from typing import Any, Dict, List, Optional, Callable
from contextlib import contextmanager
from functools import wraps
import threading


class CachePolicy:
    """キャッシュポリシー定数"""
    LRU = "LRU"  # Least Recently Used
    LFU = "LFU"  # Least Frequently Used
    FIFO = "FIFO"  # First In First Out
    TTL = "TTL"  # Time To Live


class HierarchicalCacheSystem:
    """EphemeralDBを使用した階層的キャッシュシステム"""
    
    def __init__(self, name: str = "キャッシュシステム"):
        self.db = EphemeralDB()
        self.name = name
        self._lock = threading.RLock()
        
        # グローバル設定
        self.db.set('システム名', name)
        self.db.set('開始時刻', time.time())
        self.db.set('統計.ヒット数', 0)
        self.db.set('統計.ミス数', 0)
        self.db.set('統計.総アクセス数', 0)
        self.db.set('キャッシュ階層', {})
    
    @contextmanager
    def cache_scope(self, scope_name: str, policy: str = CachePolicy.LRU, 
                   max_size: int = 100, ttl: float = 3600):
        """キャッシュスコープのコンテキストマネージャー"""
        with self.db.scope(f'キャッシュ_{scope_name}'):
            # スコープ設定を初期化
            self.db.set('スコープ名', scope_name)
            self.db.set('ポリシー', policy)
            self.db.set('最大サイズ', max_size)
            self.db.set('TTL', ttl)
            self.db.set('作成時刻', time.time())
            self.db.set('データ', {})
            self.db.set('メタデータ', {})
            self.db.set('アクセス履歴', [])
            self.db.set('統計', {
                'ヒット数': 0,
                'ミス数': 0,
                'エビクション数': 0
            })
            
            print(f"キャッシュスコープ '{scope_name}' を開始 (ポリシー: {policy}, 最大サイズ: {max_size})")
            
            try:
                yield self
            finally:
                # スコープ終了時の統計表示
                stats = self.db.get('統計')
                total_access = stats['ヒット数'] + stats['ミス数']
                hit_rate = (stats['ヒット数'] / total_access * 100) if total_access > 0 else 0
                print(f"キャッシュスコープ '{scope_name}' 終了 - ヒット率: {hit_rate:.1f}%")
    
    def get(self, key: str, default: Any = None) -> Any:
        """キャッシュからデータを取得"""
        with self._lock:
            # 統計更新
            total_access = self.db.get('統計.総アクセス数')
            self.db.set('統計.総アクセス数', total_access + 1)
            
            scope_stats = self.db.get('統計')
            
            data = self.db.get('データ', {})
            metadata = self.db.get('メタデータ', {})
            
            if key not in data:
                # キャッシュミス
                scope_stats['ミス数'] += 1
                self.db.set('統計', scope_stats)
                
                global_miss = self.db.get('統計.ミス数')
                self.db.set('統計.ミス数', global_miss + 1)
                
                self._record_access(key, 'MISS')
                return default
            
            # TTLチェック
            if self._is_expired(key, metadata):
                # 期限切れ
                self._remove_key(key)
                scope_stats['ミス数'] += 1
                self.db.set('統計', scope_stats)
                
                global_miss = self.db.get('統計.ミス数')
                self.db.set('統計.ミス数', global_miss + 1)
                
                self._record_access(key, 'EXPIRED')
                return default
            
            # キャッシュヒット
            scope_stats['ヒット数'] += 1
            self.db.set('統計', scope_stats)
            
            global_hit = self.db.get('統計.ヒット数')
            self.db.set('統計.ヒット数', global_hit + 1)
            
            # アクセス情報更新
            self._update_access_info(key, metadata)
            self._record_access(key, 'HIT')
            
            return data[key]
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """キャッシュにデータを設定"""
        with self._lock:
            data = self.db.get('データ', {})
            metadata = self.db.get('メタデータ', {})
            max_size = self.db.get('最大サイズ')
            policy = self.db.get('ポリシー')
            default_ttl = self.db.get('TTL')
            
            # 既存キーの場合は更新
            if key in data:
                data[key] = value
                self._update_metadata(key, metadata, ttl or default_ttl)
                self.db.set('データ', data)
                self.db.set('メタデータ', metadata)
                self._record_access(key, 'UPDATE')
                return
            
            # 新規キー追加
            # サイズチェックとエビクション
            if len(data) >= max_size:
                evicted_key = self._evict_one(policy, data, metadata)
                if evicted_key:
                    scope_stats = self.db.get('統計')
                    scope_stats['エビクション数'] += 1
                    self.db.set('統計', scope_stats)
                    self._record_access(evicted_key, 'EVICTED')
            
            # データ追加
            data[key] = value
            self._update_metadata(key, metadata, ttl or default_ttl)
            
            self.db.set('データ', data)
            self.db.set('メタデータ', metadata)
            self._record_access(key, 'SET')
    
    def delete(self, key: str) -> bool:
        """キャッシュからデータを削除"""
        with self._lock:
            data = self.db.get('データ', {})
            
            if key in data:
                self._remove_key(key)
                self._record_access(key, 'DELETE')
                return True
            
            return False
    
    def clear(self) -> None:
        """キャッシュをクリア"""
        with self._lock:
            self.db.set('データ', {})
            self.db.set('メタデータ', {})
            self._record_access('*', 'CLEAR')
    
    def size(self) -> int:
        """現在のキャッシュサイズ"""
        data = self.db.get('データ', {})
        return len(data)
    
    def keys(self) -> List[str]:
        """キャッシュ内の全キー"""
        data = self.db.get('データ', {})
        return list(data.keys())
    
    def cached_function(self, ttl: Optional[float] = None, key_func: Optional[Callable] = None):
        """関数キャッシュデコレータ"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # キャッシュキー生成
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    cache_key = self._generate_function_key(func.__name__, args, kwargs)
                
                # キャッシュから取得試行
                result = self.get(cache_key)
                if result is not None:
                    return result
                
                # 関数実行
                result = func(*args, **kwargs)
                
                # 結果をキャッシュ
                self.set(cache_key, result, ttl)
                
                return result
            
            return wrapper
        return decorator
    
    def _is_expired(self, key: str, metadata: Dict) -> bool:
        """キーが期限切れかチェック"""
        if key not in metadata:
            return False
        
        key_meta = metadata[key]
        if 'expires_at' not in key_meta:
            return False
        
        return time.time() > key_meta['expires_at']
    
    def _update_access_info(self, key: str, metadata: Dict) -> None:
        """アクセス情報を更新"""
        if key not in metadata:
            return
        
        key_meta = metadata[key]
        key_meta['last_accessed'] = time.time()
        key_meta['access_count'] = key_meta.get('access_count', 0) + 1
        
        self.db.set('メタデータ', metadata)
    
    def _update_metadata(self, key: str, metadata: Dict, ttl: float) -> None:
        """メタデータを更新"""
        now = time.time()
        
        metadata[key] = {
            'created_at': now,
            'last_accessed': now,
            'access_count': 1,
            'expires_at': now + ttl,
            'ttl': ttl
        }
    
    def _evict_one(self, policy: str, data: Dict, metadata: Dict) -> Optional[str]:
        """ポリシーに基づいて一つのアイテムをエビクション"""
        if not data:
            return None
        
        if policy == CachePolicy.LRU:
            # 最も古くアクセスされたアイテム
            oldest_key = min(metadata.keys(), 
                           key=lambda k: metadata[k].get('last_accessed', 0))
            self._remove_key(oldest_key)
            return oldest_key
        
        elif policy == CachePolicy.LFU:
            # 最もアクセス頻度の低いアイテム
            least_used_key = min(metadata.keys(), 
                                key=lambda k: metadata[k].get('access_count', 0))
            self._remove_key(least_used_key)
            return least_used_key
        
        elif policy == CachePolicy.FIFO:
            # 最も古く作成されたアイテム
            oldest_key = min(metadata.keys(), 
                           key=lambda k: metadata[k].get('created_at', 0))
            self._remove_key(oldest_key)
            return oldest_key
        
        else:
            # デフォルトは最初のキー
            first_key = next(iter(data.keys()))
            self._remove_key(first_key)
            return first_key
    
    def _remove_key(self, key: str) -> None:
        """キーを削除"""
        data = self.db.get('データ', {})
        metadata = self.db.get('メタデータ', {})
        
        if key in data:
            del data[key]
        if key in metadata:
            del metadata[key]
        
        self.db.set('データ', data)
        self.db.set('メタデータ', metadata)
    
    def _record_access(self, key: str, action: str) -> None:
        """アクセスを記録"""
        access_history = self.db.get('アクセス履歴', [])
        access_history.append({
            '時刻': time.time(),
            'キー': key,
            'アクション': action,
            'スコープ': self.db.current_scope()
        })
        
        # 履歴が長くなりすぎないよう制限
        if len(access_history) > 1000:
            access_history = access_history[-500:]
        
        self.db.set('アクセス履歴', access_history)
    
    def _generate_function_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """関数引数からキャッシュキーを生成"""
        # 引数を文字列に変換
        args_str = json.dumps(args, sort_keys=True, default=str)
        kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
        
        # ハッシュ化
        content = f"{func_name}:{args_str}:{kwargs_str}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_statistics(self) -> Dict[str, Any]:
        """統計情報を取得"""
        scope_stats = self.db.get('統計', {})
        global_hit = self.db.get('統計.ヒット数', 0)
        global_miss = self.db.get('統計.ミス数', 0)
        total_access = global_hit + global_miss
        
        return {
            'スコープ統計': scope_stats,
            'グローバル統計': {
                'ヒット数': global_hit,
                'ミス数': global_miss,
                '総アクセス数': total_access,
                'ヒット率': (global_hit / total_access * 100) if total_access > 0 else 0
            },
            '現在のサイズ': self.size(),
            '最大サイズ': self.db.get('最大サイズ', 0)
        }


def basic_cache_demo():
    """基本的なキャッシュ機能のデモ"""
    print("=== 基本キャッシュ機能 ===")
    
    cache = HierarchicalCacheSystem("基本キャッシュ")
    
    with cache.cache_scope("ユーザーデータ", policy=CachePolicy.LRU, max_size=5):
        # データ設定
        cache.set("user:1", {"名前": "田中太郎", "年齢": 30})
        cache.set("user:2", {"名前": "佐藤花子", "年齢": 25})
        cache.set("user:3", {"名前": "鈴木一郎", "年齢": 35})
        
        print(f"キャッシュサイズ: {cache.size()}")
        
        # データ取得
        user1 = cache.get("user:1")
        print(f"ユーザー1: {user1}")
        
        user4 = cache.get("user:4", "見つかりません")
        print(f"ユーザー4: {user4}")
        
        # 統計表示
        stats = cache.get_statistics()
        print(f"統計: {stats['スコープ統計']}")
    
    print()


def cache_policy_demo():
    """キャッシュポリシーのデモ"""
    print("=== キャッシュポリシーのデモ ===")
    
    cache = HierarchicalCacheSystem("ポリシーテスト")
    
    # LRUポリシーのテスト
    print("--- LRUポリシー ---")
    with cache.cache_scope("LRUテスト", policy=CachePolicy.LRU, max_size=3):
        # キャッシュを満杯にする
        for i in range(1, 4):
            cache.set(f"key{i}", f"value{i}")
        
        print(f"初期キー: {cache.keys()}")
        
        # key1をアクセス（最近使用に）
        cache.get("key1")
        
        # 新しいキーを追加（key2が最も古いアクセスなのでエビクション）
        cache.set("key4", "value4")
        print(f"key4追加後: {cache.keys()}")
    
    # LFUポリシーのテスト
    print("\n--- LFUポリシー ---")
    with cache.cache_scope("LFUテスト", policy=CachePolicy.LFU, max_size=3):
        # キャッシュを設定
        cache.set("frequent", "よくアクセス")
        cache.set("rare", "あまりアクセスしない")
        cache.set("medium", "普通")
        
        # 頻度を変える
        for _ in range(5):
            cache.get("frequent")
        for _ in range(2):
            cache.get("medium")
        
        # 新しいキーを追加（rareが最も使用頻度が低いのでエビクション）
        cache.set("new", "新しい")
        print(f"new追加後: {cache.keys()}")
    
    print()


def hierarchical_cache_demo():
    """階層的キャッシュのデモ"""
    print("=== 階層的キャッシュ ===")
    
    cache = HierarchicalCacheSystem("階層キャッシュ")
    
    # レベル1: アプリケーションレベル
    with cache.cache_scope("アプリケーション", max_size=100, ttl=3600):
        cache.set("アプリ設定", {"デバッグ": True, "バージョン": "1.0"})
        
        # レベル2: セッションレベル
        with cache.cache_scope("セッション", max_size=50, ttl=1800):
            cache.set("ユーザーID", "user123")
            cache.set("認証トークン", "token_abc123")
            
            # レベル3: リクエストレベル
            with cache.cache_scope("リクエスト", max_size=20, ttl=300):
                cache.set("リクエストID", "req_001")
                cache.set("処理開始時刻", time.time())
                
                # 各レベルからデータにアクセス
                print(f"アプリ設定: {cache.get('アプリ設定')}")  # レベル1から継承
                print(f"ユーザーID: {cache.get('ユーザーID')}")    # レベル2から継承
                print(f"リクエストID: {cache.get('リクエストID')}")  # レベル3
                
                # 統計確認
                stats = cache.get_statistics()
                print(f"リクエストレベル統計: {stats['スコープ統計']}")
            
            print("リクエストスコープ終了")
            # リクエストレベルのデータは削除されているが、上位レベルは残る
            print(f"ユーザーID（セッションレベル）: {cache.get('ユーザーID')}")
        
        print("セッションスコープ終了")
        print(f"アプリ設定（アプリケーションレベル）: {cache.get('アプリ設定')}")
    
    print()


def function_caching_demo():
    """関数キャッシュのデモ"""
    print("=== 関数キャッシュ ===")
    
    cache = HierarchicalCacheSystem("関数キャッシュ")
    
    with cache.cache_scope("計算結果", max_size=10, ttl=60):
        
        @cache.cached_function(ttl=30)
        def expensive_calculation(n: int) -> int:
            """重い計算のシミュレーション"""
            print(f"重い計算実行: {n}")
            time.sleep(0.1)  # 重い処理をシミュレート
            return n * n * n
        
        @cache.cached_function()
        def fibonacci(n: int) -> int:
            """フィボナッチ数列（キャッシュ付き）"""
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)
        
        # 関数呼び出しテスト
        print("=== 重い計算テスト ===")
        start_time = time.time()
        result1 = expensive_calculation(10)
        first_time = time.time() - start_time
        print(f"初回実行: {result1} ({first_time:.3f}秒)")
        
        start_time = time.time()
        result2 = expensive_calculation(10)  # キャッシュヒット
        second_time = time.time() - start_time
        print(f"2回目実行: {result2} ({second_time:.3f}秒)")
        
        print(f"速度向上: {first_time / second_time:.1f}倍")
        
        print("\n=== フィボナッチテスト ===")
        start_time = time.time()
        fib_result = fibonacci(10)
        fib_time = time.time() - start_time
        print(f"fibonacci(10) = {fib_result} ({fib_time:.3f}秒)")
        
        # 統計表示
        stats = cache.get_statistics()
        print(f"関数キャッシュ統計: {stats['スコープ統計']}")
    
    print()


def ttl_cache_demo():
    """TTL（Time To Live）キャッシュのデモ"""
    print("=== TTL キャッシュ ===")
    
    cache = HierarchicalCacheSystem("TTLキャッシュ")
    
    with cache.cache_scope("TTLテスト", max_size=10, ttl=2):  # 2秒のTTL
        # データ設定
        cache.set("短期データ", "2秒で期限切れ")
        cache.set("長期データ", "10秒で期限切れ", ttl=10)
        
        print("データ設定完了")
        print(f"短期データ: {cache.get('短期データ')}")
        print(f"長期データ: {cache.get('長期データ')}")
        
        # 1秒待機
        print("\n1秒待機...")
        time.sleep(1)
        
        print(f"短期データ（1秒後）: {cache.get('短期データ')}")
        print(f"長期データ（1秒後）: {cache.get('長期データ')}")
        
        # さらに2秒待機（合計3秒）
        print("\nさらに2秒待機...")
        time.sleep(2)
        
        print(f"短期データ（3秒後）: {cache.get('短期データ', 'EXPIRED')}")
        print(f"長期データ（3秒後）: {cache.get('長期データ')}")
        
        # 統計表示
        stats = cache.get_statistics()
        print(f"TTL統計: {stats['スコープ統計']}")
    
    print()


def performance_comparison_demo():
    """パフォーマンス比較デモ"""
    print("=== パフォーマンス比較 ===")
    
    cache = HierarchicalCacheSystem("パフォーマンステスト")
    
    def slow_database_query(query_id: int) -> Dict[str, Any]:
        """重いデータベースクエリのシミュレーション"""
        time.sleep(0.01)  # 10msの遅延をシミュレート
        return {
            "id": query_id,
            "データ": f"クエリ{query_id}の結果",
            "取得時刻": time.time()
        }
    
    with cache.cache_scope("データベースキャッシュ", max_size=20):
        
        @cache.cached_function()
        def cached_query(query_id: int) -> Dict[str, Any]:
            return slow_database_query(query_id)
        
        # キャッシュなしでのテスト
        print("--- キャッシュなしテスト ---")
        start_time = time.time()
        for i in range(5):
            result = slow_database_query(1)  # 同じクエリを繰り返し
        no_cache_time = time.time() - start_time
        print(f"キャッシュなし（5回）: {no_cache_time:.3f}秒")
        
        # キャッシュありでのテスト
        print("\n--- キャッシュありテスト ---")
        start_time = time.time()
        for i in range(5):
            result = cached_query(1)  # 同じクエリを繰り返し
        cache_time = time.time() - start_time
        print(f"キャッシュあり（5回）: {cache_time:.3f}秒")
        
        # 速度向上計算
        improvement = no_cache_time / cache_time
        print(f"速度向上: {improvement:.1f}倍")
        
        # 異なるクエリでのテスト
        print("\n--- 異なるクエリテスト ---")
        for query_id in range(1, 6):
            start_time = time.time()
            result = cached_query(query_id)
            exec_time = time.time() - start_time
            print(f"クエリ{query_id}: {exec_time:.3f}秒")
        
        # 最終統計
        stats = cache.get_statistics()
        print(f"\n最終統計: {stats['グローバル統計']}")
    
    print()


if __name__ == "__main__":
    basic_cache_demo()
    cache_policy_demo()
    hierarchical_cache_demo()
    function_caching_demo()
    ttl_cache_demo()
    performance_comparison_demo()
    
    print("=== まとめ ===")
    print("EphemeralDBを使用することで、高度な階層的キャッシュ")
    print("システムを構築できます。異なるキャッシュポリシー、")
    print("TTL管理、関数キャッシュなど、実用的な機能を")
    print("スコープ管理により効率的に実装できます。")