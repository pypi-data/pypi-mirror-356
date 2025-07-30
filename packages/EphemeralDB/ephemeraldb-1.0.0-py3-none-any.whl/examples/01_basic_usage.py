#!/usr/bin/env python3
"""
01. 基本的な使用方法 - EphemeralDBの基本操作を学ぶ
"""

from ephemeraldb import EphemeralDB


def basic_operations():
    """基本的なCRUD操作のデモンストレーション"""
    print("=== 基本操作 ===")
    
    db = EphemeralDB()
    
    # 様々なデータ型の保存
    db.set('名前', 'アリス')
    db.set('年齢', 30)
    db.set('設定', {'テーマ': '暗い', '言語': '日本語'})
    db.set('スコア', [85, 92, 78])
    
    # データの取得
    print(f"名前: {db.get('名前')}")
    print(f"年齢: {db.get('年齢')}")
    print(f"設定: {db.get('設定')}")
    print(f"スコア: {db.get('スコア')}")
    
    # 存在確認
    print(f"'名前'が存在: {db.exists('名前')}")
    print(f"'不明'が存在: {db.exists('不明')}")
    
    # データの削除
    db.delete('年齢')
    print(f"削除後の年齢: {db.get('年齢')}")
    
    print()


def nested_keys():
    """ネストしたキー操作のデモンストレーション"""
    print("=== ネストしたキー ===")
    
    db = EphemeralDB()
    
    # ドット記法でネストしたデータを設定
    db.set('ユーザー.プロフィール.名前', 'ボブ')
    db.set('ユーザー.プロフィール.メール', 'bob@example.com')
    db.set('ユーザー.設定.テーマ', '明い')
    db.set('ユーザー.設定.通知', True)
    
    # ネストしたデータにアクセス
    print(f"ユーザー名: {db.get('ユーザー.プロフィール.名前')}")
    print(f"メール: {db.get('ユーザー.プロフィール.メール')}")
    print(f"テーマ: {db.get('ユーザー.設定.テーマ')}")
    print(f"通知: {db.get('ユーザー.設定.通知')}")
    
    # 全キーのリスト
    print(f"全キー: {db.keys()}")
    
    print()


def default_values():
    """デフォルト値の使用例"""
    print("=== デフォルト値 ===")
    
    db = EphemeralDB()
    
    # 存在しないキーにデフォルト値を設定
    print(f"存在しないキー: {db.get('存在しない')}")
    print(f"デフォルト値付き: {db.get('存在しない', 'デフォルト')}")
    print(f"数値デフォルト: {db.get('存在しない', 42)}")
    
    # 設定されたキーはデフォルト値を無視
    db.set('設定済み', '実際の値')
    print(f"設定済みキー: {db.get('設定済み', 'デフォルト')}")
    
    print()


def data_types():
    """様々なデータ型の保存と取得"""
    print("=== データ型 ===")
    
    db = EphemeralDB()
    
    # 様々なデータ型をテスト
    test_data = {
        '文字列': 'これは文字列です',
        '整数': 42,
        '浮動小数点': 3.14159,
        'ブール値': True,
        'リスト': [1, 2, 3, '混合', True],
        '辞書': {
            'ネスト': {
                '深い': 'ネスト構造',
                '数値': 100
            }
        },
        'タプル': (1, 2, 3),
        'None値': None
    }
    
    # データを保存
    for key, value in test_data.items():
        db.set(key, value)
    
    # データを取得して型を確認
    for key in test_data.keys():
        value = db.get(key)
        print(f"{key}: {value} (型: {type(value).__name__})")
    
    print()


if __name__ == "__main__":
    basic_operations()
    nested_keys()
    default_values()
    data_types()
    
    print("=== まとめ ===")
    print("EphemeralDBは様々なデータ型を保存でき、")
    print("ドット記法でネストしたキーもサポートします。")
    print("デフォルト値を使用して安全にデータにアクセスできます。")