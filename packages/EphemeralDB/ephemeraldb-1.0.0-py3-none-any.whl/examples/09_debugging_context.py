#!/usr/bin/env python3
"""
09. デバッグコンテキスト - デバッグ情報を管理するシステム
"""

from ephemeraldb import EphemeralDB
import time
import traceback
import sys
from typing import Any, Dict, List, Optional, Callable
from contextlib import contextmanager
from functools import wraps


class DebugLevel:
    """デバッグレベル定数"""
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class DebugContext:
    """EphemeralDBを使用したデバッグコンテキスト管理"""
    
    def __init__(self, name: str = "アプリケーション"):
        self.db = EphemeralDB()
        self.name = name
        
        # グローバル設定
        self.db.set('アプリ名', name)
        self.db.set('開始時刻', time.time())
        self.db.set('デバッグレベル', DebugLevel.INFO)
        self.db.set('ログ履歴', [])
        self.db.set('エラー履歴', [])
        self.db.set('パフォーマンス統計', {})
        self.db.set('呼び出しスタック', [])
    
    def set_debug_level(self, level: int):
        """デバッグレベルを設定"""
        self.db.set('デバッグレベル', level)
        level_names = ['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        level_name = level_names[level] if 0 <= level < len(level_names) else 'UNKNOWN'
        print(f"デバッグレベルを{level_name}に設定")
    
    @contextmanager
    def function_scope(self, function_name: str, **kwargs):
        """関数スコープのコンテキストマネージャー"""
        with self.db.scope(f'関数_{function_name}'):
            start_time = time.time()
            
            # 関数情報を設定
            self.db.set('関数名', function_name)
            self.db.set('開始時刻', start_time)
            self.db.set('引数', kwargs)
            self.db.set('ローカル変数', {})
            self.db.set('実行ログ', [])
            
            # 呼び出しスタックに追加
            call_stack = self.db.get('呼び出しスタック')
            call_stack.append({
                '関数名': function_name,
                '開始時刻': start_time,
                '引数': kwargs
            })
            self.db.set('呼び出しスタック', call_stack)
            
            self.log(DebugLevel.DEBUG, f"関数 {function_name} 開始", kwargs)
            
            try:
                yield self
                
                # 正常終了
                end_time = time.time()
                execution_time = end_time - start_time
                
                self.db.set('終了時刻', end_time)
                self.db.set('実行時間', execution_time)
                self.db.set('正常終了', True)
                
                self.log(DebugLevel.DEBUG, f"関数 {function_name} 正常終了", {
                    '実行時間': f'{execution_time:.4f}秒'
                })
                
                # パフォーマンス統計更新
                self._update_performance_stats(function_name, execution_time)
                
            except Exception as e:
                # 例外発生
                end_time = time.time()
                execution_time = end_time - start_time
                
                self.db.set('終了時刻', end_time)
                self.db.set('実行時間', execution_time)
                self.db.set('正常終了', False)
                self.db.set('例外', {
                    'タイプ': type(e).__name__,
                    'メッセージ': str(e),
                    'トレースバック': traceback.format_exc()
                })
                
                self.log(DebugLevel.ERROR, f"関数 {function_name} で例外発生", {
                    '例外タイプ': type(e).__name__,
                    'メッセージ': str(e),
                    '実行時間': f'{execution_time:.4f}秒'
                })
                
                # エラー履歴に記録
                self._record_error(function_name, e, execution_time)
                
                raise
            
            finally:
                # 呼び出しスタックから削除
                call_stack = self.db.get('呼び出しスタック')
                if call_stack:
                    call_stack.pop()
                    self.db.set('呼び出しスタック', call_stack)
    
    def log(self, level: int, message: str, data: Optional[Dict[str, Any]] = None):
        """ログメッセージを記録"""
        current_level = self.db.get('デバッグレベル')
        if level < current_level:
            return
        
        # ログエントリ作成
        log_entry = {
            '時刻': time.time(),
            'レベル': level,
            'メッセージ': message,
            'データ': data or {},
            'スコープ': self.db.current_scope(),
            'スタック深度': len(self.db.get('呼び出しスタック', []))
        }
        
        # 現在のスコープのログに追加
        execution_log = self.db.get('実行ログ', [])
        execution_log.append(log_entry)
        self.db.set('実行ログ', execution_log)
        
        # グローバルログ履歴に追加
        log_history = self.db.get('ログ履歴')
        log_history.append(log_entry)
        self.db.set('ログ履歴', log_history)
        
        # コンソール出力
        level_names = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRIT']
        level_name = level_names[level] if 0 <= level < len(level_names) else 'UNK'
        indent = '  ' * log_entry['スタック深度']
        
        print(f"{indent}[{level_name}] {message}")
        if data:
            for key, value in data.items():
                print(f"{indent}    {key}: {value}")
    
    def set_variable(self, name: str, value: Any):
        """ローカル変数を設定"""
        local_vars = self.db.get('ローカル変数', {})
        local_vars[name] = value
        self.db.set('ローカル変数', local_vars)
        
        self.log(DebugLevel.TRACE, f"変数設定: {name}", {'値': value})
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """ローカル変数を取得"""
        local_vars = self.db.get('ローカル変数', {})
        value = local_vars.get(name, default)
        
        self.log(DebugLevel.TRACE, f"変数取得: {name}", {'値': value})
        return value
    
    def checkpoint(self, name: str, data: Optional[Dict[str, Any]] = None):
        """チェックポイントを設定"""
        checkpoint_data = {
            '名前': name,
            '時刻': time.time(),
            'データ': data or {},
            'ローカル変数': self.db.get('ローカル変数', {}),
            'スコープ': self.db.current_scope()
        }
        
        checkpoints = self.db.get('チェックポイント', [])
        checkpoints.append(checkpoint_data)
        self.db.set('チェックポイント', checkpoints)
        
        self.log(DebugLevel.DEBUG, f"チェックポイント: {name}", data)
    
    def assert_condition(self, condition: bool, message: str, data: Optional[Dict[str, Any]] = None):
        """アサーション"""
        if not condition:
            self.log(DebugLevel.ERROR, f"アサーション失敗: {message}", data)
            raise AssertionError(message)
        else:
            self.log(DebugLevel.TRACE, f"アサーション成功: {message}", data)
    
    def _update_performance_stats(self, function_name: str, execution_time: float):
        """パフォーマンス統計更新"""
        stats = self.db.get('パフォーマンス統計')
        
        if function_name not in stats:
            stats[function_name] = {
                '実行回数': 0,
                '総実行時間': 0.0,
                '最小実行時間': float('inf'),
                '最大実行時間': 0.0
            }
        
        func_stats = stats[function_name]
        func_stats['実行回数'] += 1
        func_stats['総実行時間'] += execution_time
        func_stats['最小実行時間'] = min(func_stats['最小実行時間'], execution_time)
        func_stats['最大実行時間'] = max(func_stats['最大実行時間'], execution_time)
        func_stats['平均実行時間'] = func_stats['総実行時間'] / func_stats['実行回数']
        
        self.db.set('パフォーマンス統計', stats)
    
    def _record_error(self, function_name: str, exception: Exception, execution_time: float):
        """エラー記録"""
        error_record = {
            '時刻': time.time(),
            '関数名': function_name,
            '例外タイプ': type(exception).__name__,
            'メッセージ': str(exception),
            '実行時間': execution_time,
            'トレースバック': traceback.format_exc(),
            'スコープ': self.db.current_scope()
        }
        
        error_history = self.db.get('エラー履歴')
        error_history.append(error_record)
        self.db.set('エラー履歴', error_history)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """パフォーマンス統計取得"""
        return self.db.get('パフォーマンス統計', {})
    
    def get_error_history(self) -> List[Dict[str, Any]]:
        """エラー履歴取得"""
        return self.db.get('エラー履歴', [])
    
    def get_log_history(self) -> List[Dict[str, Any]]:
        """ログ履歴取得"""
        return self.db.get('ログ履歴', [])
    
    def print_summary(self):
        """デバッグサマリーを出力"""
        print("\n=== デバッグサマリー ===")
        
        # パフォーマンス統計
        stats = self.get_performance_stats()
        if stats:
            print("\nパフォーマンス統計:")
            for func_name, func_stats in stats.items():
                print(f"  {func_name}:")
                print(f"    実行回数: {func_stats['実行回数']}回")
                print(f"    平均実行時間: {func_stats['平均実行時間']:.4f}秒")
                print(f"    最小/最大: {func_stats['最小実行時間']:.4f}秒 / {func_stats['最大実行時間']:.4f}秒")
        
        # エラー統計
        errors = self.get_error_history()
        if errors:
            print(f"\nエラー統計: {len(errors)}件のエラー")
            error_types = {}
            for error in errors:
                error_type = error['例外タイプ']
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            for error_type, count in error_types.items():
                print(f"  {error_type}: {count}件")
        
        # ログ統計
        logs = self.get_log_history()
        if logs:
            print(f"\nログ統計: {len(logs)}件のログ")
            level_counts = {}
            level_names = ['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            
            for log in logs:
                level = log['レベル']
                level_name = level_names[level] if 0 <= level < len(level_names) else 'UNKNOWN'
                level_counts[level_name] = level_counts.get(level_name, 0) + 1
            
            for level_name, count in level_counts.items():
                print(f"  {level_name}: {count}件")


def debug_decorator(debug_context: DebugContext):
    """デバッグ用デコレータ"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with debug_context.function_scope(func.__name__, 引数=args, キーワード引数=kwargs):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def basic_debugging_demo():
    """基本的なデバッグ機能のデモ"""
    print("=== 基本デバッグ機能 ===")
    
    debug = DebugContext("計算アプリ")
    debug.set_debug_level(DebugLevel.DEBUG)
    
    @debug_decorator(debug)
    def add_numbers(a: int, b: int) -> int:
        debug.set_variable('a', a)
        debug.set_variable('b', b)
        
        debug.checkpoint("引数チェック", {'a': a, 'b': b})
        debug.assert_condition(isinstance(a, (int, float)), "aは数値である必要があります")
        debug.assert_condition(isinstance(b, (int, float)), "bは数値である必要があります")
        
        result = a + b
        debug.set_variable('result', result)
        
        debug.checkpoint("計算完了", {'result': result})
        debug.log(DebugLevel.INFO, "加算処理完了", {'結果': result})
        
        return result
    
    @debug_decorator(debug)
    def multiply_numbers(a: int, b: int) -> int:
        debug.set_variable('a', a)
        debug.set_variable('b', b)
        
        # add_numbers を呼び出し（ネストしたデバッグコンテキスト）
        temp_result = add_numbers(a, 0)  # a + 0 = a
        
        result = a * b
        debug.set_variable('result', result)
        
        debug.log(DebugLevel.INFO, "乗算処理完了", {'結果': result})
        return result
    
    # 正常なケース
    result1 = add_numbers(10, 20)
    print(f"加算結果: {result1}")
    
    result2 = multiply_numbers(5, 4)
    print(f"乗算結果: {result2}")
    
    # エラーケース
    try:
        add_numbers("文字列", 20)
    except AssertionError as e:
        print(f"エラーをキャッチ: {e}")
    
    debug.print_summary()
    print()


def complex_algorithm_debugging():
    """複雑なアルゴリズムのデバッグ"""
    print("=== 複雑なアルゴリズムのデバッグ ===")
    
    debug = DebugContext("ソートアルゴリズム")
    debug.set_debug_level(DebugLevel.INFO)
    
    @debug_decorator(debug)
    def bubble_sort(arr: List[int]) -> List[int]:
        debug.set_variable('original_array', arr.copy())
        debug.set_variable('array_length', len(arr))
        
        arr = arr.copy()  # 元の配列を変更しない
        n = len(arr)
        
        debug.checkpoint("ソート開始", {'配列長': n, '元の配列': arr})
        
        for i in range(n):
            debug.log(DebugLevel.DEBUG, f"外側ループ {i+1}/{n}")
            
            with debug.db.scope(f'外側ループ_{i}'):
                debug.set_variable('outer_index', i)
                swapped = False
                
                for j in range(0, n - i - 1):
                    with debug.db.scope(f'内側ループ_{j}'):
                        debug.set_variable('inner_index', j)
                        debug.set_variable('comparing', [arr[j], arr[j + 1]])
                        
                        if arr[j] > arr[j + 1]:
                            # スワップ
                            debug.log(DebugLevel.TRACE, f"スワップ: {arr[j]} <-> {arr[j + 1]}")
                            arr[j], arr[j + 1] = arr[j + 1], arr[j]
                            swapped = True
                            
                            debug.checkpoint("スワップ実行", {
                                'インデックス': [j, j + 1],
                                '現在の配列': arr.copy()
                            })
                
                debug.set_variable('swapped_in_pass', swapped)
                
                if not swapped:
                    debug.log(DebugLevel.INFO, f"第{i+1}パスでスワップなし - ソート完了")
                    break
                
                debug.checkpoint(f"第{i+1}パス完了", {'配列状態': arr.copy()})
        
        debug.checkpoint("ソート完了", {'最終配列': arr})
        debug.log(DebugLevel.INFO, "バブルソート完了", {'結果': arr})
        
        return arr
    
    @debug_decorator(debug)
    def find_max(arr: List[int]) -> Dict[str, Any]:
        debug.set_variable('array', arr)
        debug.assert_condition(len(arr) > 0, "配列が空です")
        
        max_value = arr[0]
        max_index = 0
        
        debug.checkpoint("最大値検索開始", {'初期値': max_value})
        
        for i, value in enumerate(arr[1:], 1):
            with debug.db.scope(f'要素_{i}'):
                debug.set_variable('current_value', value)
                debug.set_variable('current_max', max_value)
                
                if value > max_value:
                    debug.log(DebugLevel.DEBUG, f"新しい最大値発見: {value} > {max_value}")
                    max_value = value
                    max_index = i
                    
                    debug.checkpoint("最大値更新", {
                        '新しい最大値': max_value,
                        'インデックス': max_index
                    })
        
        result = {'値': max_value, 'インデックス': max_index}
        debug.log(DebugLevel.INFO, "最大値検索完了", result)
        
        return result
    
    # テストデータ
    test_array = [64, 34, 25, 12, 22, 11, 90]
    
    print(f"元の配列: {test_array}")
    
    # 最大値検索
    max_info = find_max(test_array)
    print(f"最大値: {max_info['値']} (インデックス: {max_info['インデックス']})")
    
    # ソート実行
    sorted_array = bubble_sort(test_array)
    print(f"ソート後: {sorted_array}")
    
    debug.print_summary()
    print()


def error_handling_debugging():
    """エラーハンドリングのデバッグ"""
    print("=== エラーハンドリングのデバッグ ===")
    
    debug = DebugContext("エラーハンドリング")
    debug.set_debug_level(DebugLevel.DEBUG)
    
    @debug_decorator(debug)
    def risky_operation(value: Any) -> str:
        debug.set_variable('input_value', value)
        
        debug.checkpoint("入力検証開始")
        
        if value is None:
            debug.log(DebugLevel.WARNING, "None値が渡されました")
            raise ValueError("None値は処理できません")
        
        if isinstance(value, str) and len(value) == 0:
            debug.log(DebugLevel.WARNING, "空文字列が渡されました")
            raise ValueError("空文字列は処理できません")
        
        debug.checkpoint("入力検証完了")
        
        # 型に応じた処理
        if isinstance(value, (int, float)):
            with debug.db.scope('数値処理'):
                debug.log(DebugLevel.DEBUG, "数値として処理")
                
                if value < 0:
                    debug.log(DebugLevel.WARNING, "負の数値です")
                    raise ValueError("負の数値は処理できません")
                
                result = f"数値: {value * 2}"
                debug.checkpoint("数値処理完了", {'結果': result})
                
        elif isinstance(value, str):
            with debug.db.scope('文字列処理'):
                debug.log(DebugLevel.DEBUG, "文字列として処理")
                
                if len(value) > 10:
                    debug.log(DebugLevel.WARNING, "文字列が長すぎます")
                    raise ValueError("文字列が長すぎます（10文字以下にしてください）")
                
                result = f"文字列: {value.upper()}"
                debug.checkpoint("文字列処理完了", {'結果': result})
                
        else:
            debug.log(DebugLevel.ERROR, f"サポートされていない型: {type(value)}")
            raise TypeError(f"型 {type(value)} はサポートされていません")
        
        debug.log(DebugLevel.INFO, "処理完了", {'結果': result})
        return result
    
    # 様々なテストケース
    test_cases = [
        (5, "正常な数値"),
        ("hello", "正常な文字列"),
        (-3, "負の数値（エラー）"),
        ("", "空文字列（エラー）"),
        ("very long string that exceeds limit", "長すぎる文字列（エラー）"),
        (None, "None値（エラー）"),
        ([1, 2, 3], "リスト（エラー）")
    ]
    
    for value, description in test_cases:
        print(f"\nテスト: {description}")
        try:
            result = risky_operation(value)
            print(f"結果: {result}")
        except Exception as e:
            print(f"例外: {type(e).__name__}: {e}")
    
    debug.print_summary()
    print()


def performance_debugging():
    """パフォーマンスのデバッグ"""
    print("=== パフォーマンスのデバッグ ===")
    
    debug = DebugContext("パフォーマンステスト")
    debug.set_debug_level(DebugLevel.INFO)
    
    @debug_decorator(debug)
    def fibonacci_recursive(n: int) -> int:
        debug.set_variable('n', n)
        
        if n <= 1:
            debug.log(DebugLevel.TRACE, f"ベースケース: fibonacci({n}) = {n}")
            return n
        
        debug.checkpoint(f"再帰計算開始", {'n': n})
        
        # 再帰呼び出し
        fib_n1 = fibonacci_recursive(n - 1)
        fib_n2 = fibonacci_recursive(n - 2)
        
        result = fib_n1 + fib_n2
        debug.log(DebugLevel.TRACE, f"fibonacci({n}) = {fib_n1} + {fib_n2} = {result}")
        
        return result
    
    @debug_decorator(debug)
    def fibonacci_iterative(n: int) -> int:
        debug.set_variable('n', n)
        
        if n <= 1:
            return n
        
        a, b = 0, 1
        debug.set_variable('a', a)
        debug.set_variable('b', b)
        
        for i in range(2, n + 1):
            with debug.db.scope(f'反復_{i}'):
                debug.set_variable('iteration', i)
                a, b = b, a + b
                debug.log(DebugLevel.TRACE, f"fibonacci({i}) = {b}")
        
        debug.log(DebugLevel.DEBUG, f"反復計算完了: fibonacci({n}) = {b}")
        return b
    
    # パフォーマンス比較
    test_values = [5, 10, 15]
    
    for n in test_values:
        print(f"\nフィボナッチ数列の第{n}項を計算:")
        
        # 再帰版
        result_recursive = fibonacci_recursive(n)
        print(f"再帰版結果: {result_recursive}")
        
        # 反復版
        result_iterative = fibonacci_iterative(n)
        print(f"反復版結果: {result_iterative}")
    
    debug.print_summary()
    print()


if __name__ == "__main__":
    basic_debugging_demo()
    complex_algorithm_debugging()
    error_handling_debugging()
    performance_debugging()
    
    print("=== まとめ ===")
    print("EphemeralDBを使用することで、デバッグ情報を")
    print("階層的に管理し、詳細な実行トレースを取得できます。")
    print("関数スコープ、変数追跡、パフォーマンス測定など")
    print("開発に必要なデバッグ機能を効率的に実装できます。")