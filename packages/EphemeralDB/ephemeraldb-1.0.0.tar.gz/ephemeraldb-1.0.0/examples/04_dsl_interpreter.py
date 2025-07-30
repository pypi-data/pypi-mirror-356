#!/usr/bin/env python3
"""
04. DSLインタープリター - EphemeralDBを使用したDSL実装
"""

from ephemeraldb import EphemeralDB
from typing import List, Dict, Any, Union


class SimpleDSLInterpreter:
    """EphemeralDBを使用したシンプルなDSLインタープリター"""
    
    def __init__(self):
        self.db = EphemeralDB()
        self.functions = {
            'SET': self._set_variable,
            'GET': self._get_variable,
            'PRINT': self._print_value,
            'BLOCK': self._execute_block,
            'IF': self._execute_if,
            'WHILE': self._execute_while,
            'FUNCTION': self._define_function,
            'CALL': self._call_function,
            'ADD': self._add_numbers,
            'MULTIPLY': self._multiply_numbers,
        }
        self.user_functions = {}
    
    def execute(self, commands: List[Dict[str, Any]]) -> List[Any]:
        """DSLコマンドのリストを実行"""
        results = []
        
        for command in commands:
            cmd_type = command.get('type')
            if cmd_type in self.functions:
                result = self.functions[cmd_type](command)
                if result is not None:
                    results.append(result)
            else:
                raise ValueError(f"不明なコマンド型: {cmd_type}")
        
        return results
    
    def _set_variable(self, command: Dict[str, Any]) -> None:
        """SET 変数 値"""
        var_name = command['variable']
        value = self._evaluate_expression(command['value'])
        self.db.set(var_name, value)
        print(f"[SET] {var_name} = {value}")
    
    def _get_variable(self, command: Dict[str, Any]) -> Any:
        """GET 変数"""
        var_name = command['variable']
        value = self.db.get(var_name)
        print(f"[GET] {var_name} => {value}")
        return value
    
    def _print_value(self, command: Dict[str, Any]) -> str:
        """PRINT 式"""
        value = self._evaluate_expression(command['expression'])
        print(f"[出力] {value}")
        return str(value)
    
    def _execute_block(self, command: Dict[str, Any]) -> List[Any]:
        """BLOCK - 新しいスコープでコマンドを実行"""
        block_name = command.get('name', '無名ブロック')
        
        with self.db.scope(block_name):
            print(f"[ブロック開始] {block_name}")
            
            # ローカル変数があればインポート
            local_vars = command.get('locals', {})
            for var, value in local_vars.items():
                self.db.set(var, self._evaluate_expression(value))
                print(f"[ローカル変数] {var} = {value}")
            
            results = self.execute(command['commands'])
            print(f"[ブロック終了] {block_name}")
            return results
    
    def _execute_if(self, command: Dict[str, Any]) -> Any:
        """IF 条件 then_commands [else_commands]"""
        condition = self._evaluate_expression(command['condition'])
        print(f"[IF] 条件: {condition}")
        
        if condition:
            print("[IF] then分岐を実行")
            return self.execute(command['then_commands'])
        elif 'else_commands' in command:
            print("[IF] else分岐を実行")
            return self.execute(command['else_commands'])
        else:
            print("[IF] 実行する分岐なし")
    
    def _execute_while(self, command: Dict[str, Any]) -> List[Any]:
        """WHILE 条件 commands"""
        results = []
        max_iterations = command.get('max_iterations', 10)  # 安全のための上限
        
        iteration = 0
        print(f"[WHILE] ループ開始（最大{max_iterations}回）")
        
        while iteration < max_iterations:
            condition = self._evaluate_expression(command['condition'])
            print(f"[WHILE] 反復{iteration}: 条件 = {condition}")
            
            if not condition:
                break
            
            # 各反復を新しいスコープで実行
            with self.db.scope(f'while_反復_{iteration}'):
                self.db.set('_反復回数', iteration)
                results.extend(self.execute(command['commands']))
            
            iteration += 1
        
        print(f"[WHILE] ループ終了（{iteration}回実行）")
        return results
    
    def _define_function(self, command: Dict[str, Any]) -> None:
        """FUNCTION 名前 パラメータ commands"""
        func_name = command['name']
        self.user_functions[func_name] = {
            'parameters': command.get('parameters', []),
            'commands': command['commands']
        }
        print(f"[関数定義] {func_name} ({', '.join(command.get('parameters', []))})")
    
    def _call_function(self, command: Dict[str, Any]) -> Any:
        """CALL 関数名 引数"""
        func_name = command['function']
        
        if func_name not in self.user_functions:
            raise ValueError(f"未定義の関数: {func_name}")
        
        func_def = self.user_functions[func_name]
        arguments = [self._evaluate_expression(arg) for arg in command.get('arguments', [])]
        
        print(f"[関数呼び出し] {func_name}({', '.join(map(str, arguments))})")
        
        # 関数を新しいスコープで実行
        with self.db.scope(f'関数_{func_name}'):
            # パラメータをバインド
            for param, arg in zip(func_def['parameters'], arguments):
                self.db.set(param, arg)
                print(f"[パラメータ] {param} = {arg}")
            
            results = self.execute(func_def['commands'])
            result = results[-1] if results else None
            print(f"[関数結果] {func_name} => {result}")
            return result
    
    def _add_numbers(self, command: Dict[str, Any]) -> float:
        """ADD 数値1 数値2"""
        a = self._evaluate_expression(command['a'])
        b = self._evaluate_expression(command['b'])
        result = a + b
        print(f"[ADD] {a} + {b} = {result}")
        return result
    
    def _multiply_numbers(self, command: Dict[str, Any]) -> float:
        """MULTIPLY 数値1 数値2"""
        a = self._evaluate_expression(command['a'])
        b = self._evaluate_expression(command['b'])
        result = a * b
        print(f"[MULTIPLY] {a} * {b} = {result}")
        return result
    
    def _evaluate_expression(self, expression: Union[str, int, float, Dict]) -> Any:
        """式を評価（簡略化版）"""
        if isinstance(expression, (int, float, str, bool)):
            return expression
        elif isinstance(expression, dict):
            if expression.get('type') == 'variable':
                return self.db.get(expression['name'])
            elif expression.get('type') == 'operation':
                return self._evaluate_operation(expression)
        
        return expression
    
    def _evaluate_operation(self, operation: Dict[str, Any]) -> Any:
        """数学的/論理的操作を評価"""
        op = operation['operator']
        left = self._evaluate_expression(operation['left'])
        right = self._evaluate_expression(operation['right'])
        
        operations = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else 0,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<': lambda a, b: a < b,
            '>': lambda a, b: a > b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
            'and': lambda a, b: a and b,
            'or': lambda a, b: a or b,
        }
        
        if op in operations:
            result = operations[op](left, right)
            print(f"[演算] {left} {op} {right} = {result}")
            return result
        else:
            raise ValueError(f"未知の演算子: {op}")


def basic_variables_demo():
    """基本的な変数操作のデモ"""
    print("=== 基本変数操作 ===")
    
    interpreter = SimpleDSLInterpreter()
    
    commands = [
        {'type': 'SET', 'variable': '名前', 'value': 'アリス'},
        {'type': 'SET', 'variable': '年齢', 'value': 30},
        {'type': 'PRINT', 'expression': {'type': 'variable', 'name': '名前'}},
        {'type': 'PRINT', 'expression': {'type': 'variable', 'name': '年齢'}},
        {'type': 'GET', 'variable': '名前'},
    ]
    
    interpreter.execute(commands)
    print()


def scope_demo():
    """スコープ機能のデモ"""
    print("=== スコープ機能 ===")
    
    interpreter = SimpleDSLInterpreter()
    
    commands = [
        {'type': 'SET', 'variable': 'グローバル変数', 'value': 'グローバルです'},
        {'type': 'BLOCK', 'name': '内部スコープ', 
         'locals': {'ローカル変数': 'ローカルです'}, 
         'commands': [
             {'type': 'PRINT', 'expression': {'type': 'variable', 'name': 'グローバル変数'}},
             {'type': 'PRINT', 'expression': {'type': 'variable', 'name': 'ローカル変数'}},
             {'type': 'SET', 'variable': '一時変数', 'value': '一時的'},
             {'type': 'PRINT', 'expression': {'type': 'variable', 'name': '一時変数'}},
         ]},
        {'type': 'PRINT', 'expression': {'type': 'variable', 'name': 'グローバル変数'}},
        {'type': 'PRINT', 'expression': {'type': 'variable', 'name': '一時変数'}},  # None
    ]
    
    interpreter.execute(commands)
    print()


def conditional_demo():
    """条件分岐のデモ"""
    print("=== 条件分岐 ===")
    
    interpreter = SimpleDSLInterpreter()
    
    commands = [
        {'type': 'SET', 'variable': 'x', 'value': 10},
        {'type': 'SET', 'variable': 'y', 'value': 5},
        {'type': 'IF', 
         'condition': {'type': 'operation', 'operator': '>', 
                      'left': {'type': 'variable', 'name': 'x'}, 
                      'right': {'type': 'variable', 'name': 'y'}},
         'then_commands': [
             {'type': 'PRINT', 'expression': 'xはyより大きいです'}
         ],
         'else_commands': [
             {'type': 'PRINT', 'expression': 'xはy以下です'}
         ]
        }
    ]
    
    interpreter.execute(commands)
    print()


def function_demo():
    """関数定義と呼び出しのデモ"""
    print("=== 関数定義と呼び出し ===")
    
    interpreter = SimpleDSLInterpreter()
    
    commands = [
        # 関数を定義
        {'type': 'FUNCTION', 'name': '数値を2倍', 'parameters': ['数値'], 'commands': [
            {'type': 'MULTIPLY', 'a': {'type': 'variable', 'name': '数値'}, 'b': 2},
        ]},
        
        # 関数を呼び出し
        {'type': 'CALL', 'function': '数値を2倍', 'arguments': [21]},
        
        # より複雑な関数
        {'type': 'FUNCTION', 'name': '計算と表示', 'parameters': ['a', 'b'], 'commands': [
            {'type': 'ADD', 'a': {'type': 'variable', 'name': 'a'}, 'b': {'type': 'variable', 'name': 'b'}},
            {'type': 'SET', 'variable': '結果', 'value': {'type': 'operation', 'operator': '+', 
                     'left': {'type': 'variable', 'name': 'a'}, 
                     'right': {'type': 'variable', 'name': 'b'}}},
            {'type': 'PRINT', 'expression': {'type': 'variable', 'name': '結果'}},
            {'type': 'GET', 'variable': '結果'},
        ]},
        
        {'type': 'CALL', 'function': '計算と表示', 'arguments': [15, 25]},
    ]
    
    results = interpreter.execute(commands)
    print(f"関数の結果: {results}")
    print()


def loop_demo():
    """ループのデモ"""
    print("=== ループ処理 ===")
    
    interpreter = SimpleDSLInterpreter()
    
    commands = [
        {'type': 'SET', 'variable': 'カウンター', 'value': 0},
        {'type': 'WHILE', 
         'condition': {'type': 'operation', 'operator': '<', 
                      'left': {'type': 'variable', 'name': 'カウンター'}, 
                      'right': 3},
         'max_iterations': 5,
         'commands': [
             {'type': 'PRINT', 'expression': {'type': 'variable', 'name': 'カウンター'}},
             {'type': 'SET', 'variable': 'ループローカル', 
              'value': {'type': 'operation', 'operator': '*', 
                       'left': {'type': 'variable', 'name': 'カウンター'}, 
                       'right': 10}},
             {'type': 'PRINT', 'expression': {'type': 'variable', 'name': 'ループローカル'}},
             {'type': 'SET', 'variable': 'カウンター', 
              'value': {'type': 'operation', 'operator': '+', 
                       'left': {'type': 'variable', 'name': 'カウンター'}, 
                       'right': 1}},
         ]
        },
        {'type': 'PRINT', 'expression': 'ループ終了'},
        {'type': 'GET', 'variable': 'カウンター'},
        {'type': 'GET', 'variable': 'ループローカル'},  # None（スコープ外）
    ]
    
    interpreter.execute(commands)
    print()


def complex_program_demo():
    """複雑なプログラムのデモ"""
    print("=== 複雑なプログラム ===")
    
    interpreter = SimpleDSLInterpreter()
    
    # 階乗を計算するDSLプログラム
    commands = [
        # 階乗関数を定義（簡略版）
        {'type': 'FUNCTION', 'name': '階乗計算', 'parameters': ['n'], 'commands': [
            {'type': 'SET', 'variable': '結果', 'value': 1},
            {'type': 'SET', 'variable': 'i', 'value': 1},
            {'type': 'WHILE', 
             'condition': {'type': 'operation', 'operator': '<=', 
                          'left': {'type': 'variable', 'name': 'i'}, 
                          'right': {'type': 'variable', 'name': 'n'}},
             'max_iterations': 10,
             'commands': [
                 {'type': 'SET', 'variable': '結果', 
                  'value': {'type': 'operation', 'operator': '*', 
                           'left': {'type': 'variable', 'name': '結果'}, 
                           'right': {'type': 'variable', 'name': 'i'}}},
                 {'type': 'SET', 'variable': 'i', 
                  'value': {'type': 'operation', 'operator': '+', 
                           'left': {'type': 'variable', 'name': 'i'}, 
                           'right': 1}},
             ]
            },
            {'type': 'GET', 'variable': '結果'},
        ]},
        
        # メインプログラム
        {'type': 'BLOCK', 'name': 'メインプログラム', 'commands': [
            {'type': 'PRINT', 'expression': '階乗計算プログラム開始'},
            {'type': 'SET', 'variable': '入力', 'value': 5},
            {'type': 'PRINT', 'expression': {'type': 'variable', 'name': '入力'}},
            {'type': 'CALL', 'function': '階乗計算', 'arguments': [{'type': 'variable', 'name': '入力'}]},
            {'type': 'PRINT', 'expression': '計算完了'},
        ]},
    ]
    
    results = interpreter.execute(commands)
    print(f"最終結果: {results}")
    print()


if __name__ == "__main__":
    basic_variables_demo()
    scope_demo()
    conditional_demo()
    function_demo()
    loop_demo()
    complex_program_demo()
    
    print("=== まとめ ===")
    print("EphemeralDBにより、DSLインタープリターで")
    print("変数スコープを簡単に管理できます。")
    print("関数呼び出し、ループ、条件分岐すべてで")
    print("適切な変数の分離が実現されます。")