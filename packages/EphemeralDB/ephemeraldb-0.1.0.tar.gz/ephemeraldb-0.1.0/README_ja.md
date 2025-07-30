# EphemeralDB

軽量で揮発性のコンテキスト管理ストアです。メモリ上でスコープ付きキー・バリューストレージを提供します。

## 概要

EphemeralDBは階層的なスコープ機能を持つ一時的なデータ管理のために設計されています。以下の用途に最適です：

- DSLインタープリター
- 複雑な設定パーサー
- ネストしたトランザクション処理
- 深い再帰処理中の一時状態管理

## 主な機能

- **スコープ付きストレージ**: スタックのようにスコープをpush/pop
- **階層アクセス**: 子スコープから親スコープのデータにアクセス可能
- **ドット記法**: `user.profile.name`のようなネストしたキーをサポート
- **コンテキストマネージャー**: `with`文で使用可能
- **スレッドセーフ**: マルチスレッド環境で使用可能
- **メモリのみ**: ファイルシステムや外部依存関係不要
- **軽量**: 純Python実装

## インストール

```bash
pip install ephemeraldb
```

## クイックスタート

```python
from ephemeraldb import EphemeralDB

# 新しいデータベースインスタンスを作成
db = EphemeralDB()

# 基本的な使用方法
db.set('名前', 'アリス')
db.set('ユーザー.年齢', 30)
print(db.get('名前'))  # アリス
print(db.get('ユーザー.年齢'))  # 30

# スコープ付き使用方法
db.set('グローバル変数', 'グローバルです')

db.push_scope('スコープ1')
db.set('ローカル変数', 'ローカルです')
print(db.get('グローバル変数'))  # グローバルです（親からアクセス可能）
print(db.get('ローカル変数'))   # ローカルです

db.pop_scope()
print(db.get('ローカル変数'))   # None（スコープが削除されました）

# コンテキストマネージャー使用方法
with db.scope('一時スコープ'):
    db.set('一時データ', '一時的')
    print(db.get('一時データ'))  # 一時的
# 一時データは自動的にクリーンアップされます
```

## APIリファレンス

### コアメソッド

- `set(key: str, value: Any)` - 値を保存
- `get(key: str, default: Any = None)` - 値を取得
- `delete(key: str)` - キーを削除
- `exists(key: str)` - キーの存在確認
- `clear()` - 現在のスコープをクリア

### スコープ管理

- `push_scope(name: str = None)` - 新しいスコープを作成
- `pop_scope()` - 現在のスコープを削除
- `current_scope()` - 現在のスコープ名を取得
- `scope_count()` - アクティブなスコープ数を取得
- `scope(name: str)` - スコープ用コンテキストマネージャー

### 高度な機能

- `keys()` - 現在のスコープの全キーを取得
- `items()` - 全キー・バリューペアを取得
- `to_dict()` - 現在のスコープを辞書としてエクスポート
- `from_dict(data: dict)` - 辞書を現在のスコープにインポート

## 使用例

### DSLインタープリター

```python
from ephemeraldb import EphemeralDB

def execute_block(db, variables, statements):
    """変数スコープを持つブロックの実行をシミュレート"""
    with db.scope('ブロックスコープ'):
        # ブロック変数をインポート
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

db = EphemeralDB()
db.set('グローバル定数', 42)

results = execute_block(
    db,
    {'ローカル変数': 'ブロック1'},
    ['SET 一時変数 こんにちは', 'GET ローカル変数', 'GET 一時変数', 'GET グローバル定数']
)

print(results)  # ['ブロック1', 'こんにちは', 42]
```

### 設定パーサー

```python
def parse_config_section(db, section_name, config_data):
    """継承を持つ設定セクションの解析"""
    with db.scope(f'設定_{section_name}'):
        for key, value in config_data.items():
            db.set(f'{section_name}.{key}', value)
        
        return db.to_dict(include_hierarchy=True)

db = EphemeralDB()
db.set('デフォルト.タイムアウト', 30)
db.set('デフォルト.リトライ回数', 3)

dev_config = parse_config_section(db, '開発', {
    'ホスト': 'localhost',
    'ポート': 8000,
    'デバッグ': True
})

print(dev_config)
```

### トランザクション処理

```python
class Transaction:
    def __init__(self, db, name):
        self.db = db
        self.name = name
    
    def __enter__(self):
        self.db.push_scope(f'トランザクション_{self.name}')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.pop_scope()

db = EphemeralDB()
db.set('アカウント.残高', 1000)

try:
    with Transaction(db, '送金') as tx:
        current_balance = db.get('アカウント.残高')
        if current_balance >= 200:
            db.set('アカウント.残高', current_balance - 200)
        else:
            raise ValueError("残高不足")
except ValueError:
    print("トランザクションがロールバックされました")
```

## エラーハンドリング

EphemeralDBは詳細なエラー情報を提供します：

```python
from ephemeraldb import EphemeralDB, ValidationError, CapacityError

try:
    db = EphemeralDB(max_scopes=5)
    # ... 何らかの操作
except CapacityError as e:
    print(f"容量エラー: {e}")
    print(f"エラーコード: {e.error_code}")
    print(f"詳細: {e.details}")
```

## パフォーマンス特性

- **メモリ使用量**: 格納されたデータのサイズに比例
- **時間計算量**: 
  - 設定/取得: O(キーの深度)
  - スコープ操作: O(1)
- **スレッドセーフ**: RLockによる保護
- **容量制限**: 設定可能な上限値

## ライセンス

MIT License

## 貢献

バグ報告や機能リクエストは、GitHubのIssueでお願いします。プルリクエストも歓迎です。

## 変更履歴

詳細は[CHANGELOG.md](CHANGELOG.md)をご覧ください。