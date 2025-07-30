#!/usr/bin/env python3
"""
02. スコープ管理 - スコープのpush/pop操作を学ぶ
"""

from ephemeraldb import EphemeralDB


def basic_scope_operations():
    """基本的なスコープ操作"""
    print("=== 基本スコープ操作 ===")
    
    db = EphemeralDB()
    
    # 初期状態
    print(f"初期スコープ数: {db.scope_count()}")
    print(f"現在のスコープ: {db.current_scope()}")
    
    # グローバルデータを設定
    db.set('グローバル設定', 'プロダクション')
    db.set('アプリ名', 'マイアプリ')
    
    # 新しいスコープをプッシュ
    db.push_scope('ユーザーセッション')
    print(f"プッシュ後のスコープ数: {db.scope_count()}")
    print(f"現在のスコープ: {db.current_scope()}")
    
    # ローカルデータを設定
    db.set('ユーザーID', 123)
    db.set('セッショントークン', 'abc123')
    
    # 両方のスコープからデータにアクセス
    print(f"グローバル設定: {db.get('グローバル設定')}")  # 親スコープから
    print(f"ユーザーID: {db.get('ユーザーID')}")  # 現在のスコープから
    
    # スコープをポップ
    popped_data = db.pop_scope()
    print(f"ポップ後のスコープ数: {db.scope_count()}")
    print(f"ポップされたデータ: {popped_data}")
    
    # ローカルデータにアクセスできないことを確認
    print(f"ユーザーID（ポップ後）: {db.get('ユーザーID')}")  # None
    print(f"グローバル設定（ポップ後）: {db.get('グローバル設定')}")  # まだ利用可能
    
    print()


def nested_scopes():
    """ネストしたスコープの操作"""
    print("=== ネストしたスコープ ===")
    
    db = EphemeralDB()
    
    # レベル0（ルート）
    db.set('レベル0', 'ルート')
    
    # レベル1
    db.push_scope('レベル1')
    db.set('レベル1変数', 'レベル1の値')
    
    # レベル2
    db.push_scope('レベル2')
    db.set('レベル2変数', 'レベル2の値')
    
    # レベル3
    db.push_scope('レベル3')
    db.set('レベル3変数', 'レベル3の値')
    
    print(f"深いネストでのスコープ数: {db.scope_count()}")
    
    # 全レベルからデータにアクセス
    print(f"レベル0: {db.get('レベル0')}")
    print(f"レベル1変数: {db.get('レベル1変数')}")
    print(f"レベル2変数: {db.get('レベル2変数')}")
    print(f"レベル3変数: {db.get('レベル3変数')}")
    
    # 順番にスコープをポップ
    db.pop_scope()  # レベル3を削除
    print(f"レベル3削除後: {db.get('レベル3変数')}")  # None
    print(f"レベル2はまだ存在: {db.get('レベル2変数')}")  # まだある
    
    db.pop_scope()  # レベル2を削除
    print(f"レベル2削除後: {db.get('レベル2変数')}")  # None
    print(f"レベル1はまだ存在: {db.get('レベル1変数')}")  # まだある
    
    db.pop_scope()  # レベル1を削除
    print(f"レベル1削除後: {db.get('レベル1変数')}")  # None
    print(f"ルートはまだ存在: {db.get('レベル0')}")  # まだある
    
    print()


def scope_shadowing():
    """スコープのシャドウイング（同名変数の上書き）"""
    print("=== スコープのシャドウイング ===")
    
    db = EphemeralDB()
    
    # 共通キー名で異なる値を設定
    db.set('共通キー', '親の値')
    db.set('親専用', '親でのみ定義')
    
    print(f"プッシュ前の共通キー: {db.get('共通キー')}")
    
    # 子スコープで同じキーをシャドウ
    db.push_scope('子スコープ')
    db.set('共通キー', '子の値')  # 親の値をシャドウ
    db.set('子専用', '子でのみ定義')
    
    print(f"子スコープでの共通キー: {db.get('共通キー')}")  # 子の値
    print(f"子スコープでの親専用: {db.get('親専用')}")  # 親から継承
    print(f"子スコープでの子専用: {db.get('子専用')}")  # 子で定義
    
    # 子スコープをポップ
    db.pop_scope()
    
    print(f"ポップ後の共通キー: {db.get('共通キー')}")  # 親の値に戻る
    print(f"ポップ後の子専用: {db.get('子専用')}")  # None
    
    print()


def scope_isolation():
    """スコープの分離を確認"""
    print("=== スコープの分離 ===")
    
    db = EphemeralDB()
    
    db.set('グローバル', 'グローバル値')
    
    # 第1の子スコープ
    db.push_scope('子1')
    db.set('ローカル', '子1の値')
    print(f"子1でのローカル: {db.get('ローカル')}")
    db.pop_scope()
    
    # 第2の子スコープ
    db.push_scope('子2')
    db.set('ローカル', '子2の値')  # 同じキー名だが異なるスコープ
    print(f"子2でのローカル: {db.get('ローカル')}")
    print(f"子2でのグローバル: {db.get('グローバル')}")  # 親からアクセス可能
    db.pop_scope()
    
    # ルートスコープに戻る
    print(f"ルートでのローカル: {db.get('ローカル')}")  # None
    print(f"ルートでのグローバル: {db.get('グローバル')}")  # まだ存在
    
    print()


def scope_inspection():
    """スコープの検査機能"""
    print("=== スコープの検査 ===")
    
    db = EphemeralDB()
    
    # 複数のスコープを作成
    scope_names = ['認証', 'データ処理', '結果生成']
    
    for name in scope_names:
        db.push_scope(name)
        db.set(f'{name}_データ', f'{name}で生成されたデータ')
        
        print(f"現在のスコープ: {db.current_scope()}")
        print(f"スコープ数: {db.scope_count()}")
        print(f"現在のキー: {db.keys()}")
        print()
    
    # 逆順でスコープをポップ
    while db.scope_count() > 1:
        current = db.current_scope()
        data = db.pop_scope()
        print(f"'{current}'スコープをポップ: {data}")
    
    print(f"最終スコープ数: {db.scope_count()}")
    
    print()


if __name__ == "__main__":
    basic_scope_operations()
    nested_scopes()
    scope_shadowing()
    scope_isolation()
    scope_inspection()
    
    print("=== まとめ ===")
    print("スコープ管理により、変数の生存期間と可視性を制御できます。")
    print("子スコープは親スコープの変数にアクセスでき、")
    print("同名変数はシャドウイング（上書き）されます。")