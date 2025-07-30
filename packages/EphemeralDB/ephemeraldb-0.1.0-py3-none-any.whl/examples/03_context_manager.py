#!/usr/bin/env python3
"""
03. コンテキストマネージャー - with文を使った自動スコープ管理
"""

from ephemeraldb import EphemeralDB


def basic_context_manager():
    """基本的なコンテキストマネージャーの使用"""
    print("=== 基本的なコンテキストマネージャー ===")
    
    db = EphemeralDB()
    
    db.set('ベースデータ', 'ベース値')
    
    # コンテキストマネージャーで自動クリーンアップ
    with db.scope('処理スコープ'):
        db.set('処理中', '処理中です')
        db.set('一時結果', [1, 2, 3])
        
        print(f"スコープ内での処理中: {db.get('処理中')}")
        print(f"スコープ内でのベースデータ: {db.get('ベースデータ')}")
        print(f"現在のスコープ数: {db.scope_count()}")
    
    # コンテキスト終了後
    print(f"コンテキスト終了後の処理中: {db.get('処理中')}")  # None
    print(f"コンテキスト終了後のベースデータ: {db.get('ベースデータ')}")  # まだ存在
    print(f"最終スコープ数: {db.scope_count()}")
    
    print()


def nested_context_managers():
    """ネストしたコンテキストマネージャー"""
    print("=== ネストしたコンテキストマネージャー ===")
    
    db = EphemeralDB()
    
    db.set('グローバル', 'グローバル値')
    
    with db.scope('外側'):
        db.set('外側変数', '外側の値')
        print(f"外側スコープ数: {db.scope_count()}")
        
        with db.scope('内側'):
            db.set('内側変数', '内側の値')
            print(f"内側スコープ数: {db.scope_count()}")
            
            # 全レベルからアクセス
            print(f"グローバル: {db.get('グローバル')}")
            print(f"外側変数: {db.get('外側変数')}")
            print(f"内側変数: {db.get('内側変数')}")
        
        # 内側コンテキスト終了後
        print(f"内側終了後のスコープ数: {db.scope_count()}")
        print(f"内側変数へのアクセス: {db.get('内側変数')}")  # None
        print(f"外側変数へのアクセス: {db.get('外側変数')}")  # まだ存在
    
    # 外側コンテキスト終了後
    print(f"外側終了後のスコープ数: {db.scope_count()}")
    print(f"全変数がクリーンアップされました")
    
    print()


def exception_handling_in_context():
    """例外発生時のコンテキスト処理"""
    print("=== 例外発生時のコンテキスト処理 ===")
    
    db = EphemeralDB()
    
    db.set('安全なデータ', '保護されたデータ')
    initial_scope_count = db.scope_count()
    
    try:
        with db.scope('危険な処理'):
            db.set('一時データ', '削除される予定')
            db.set('処理状況', '進行中')
            
            print(f"例外前のスコープ数: {db.scope_count()}")
            print(f"例外前の一時データ: {db.get('一時データ')}")
            
            # 意図的に例外を発生
            raise ValueError("テスト例外")
            
    except ValueError as e:
        print(f"例外をキャッチ: {e}")
    
    # 例外後のクリーンアップ確認
    print(f"例外後のスコープ数: {db.scope_count()}")
    print(f"一時データ（クリーンアップ済み）: {db.get('一時データ')}")  # None
    print(f"安全なデータ: {db.get('安全なデータ')}")  # まだ存在
    
    assert db.scope_count() == initial_scope_count, "スコープが適切にクリーンアップされていません"
    print("例外発生時でも適切にクリーンアップされました")
    
    print()


def resource_management():
    """リソース管理パターン"""
    print("=== リソース管理パターン ===")
    
    db = EphemeralDB()
    
    def simulate_database_transaction():
        """データベーストランザクションのシミュレーション"""
        with db.scope('トランザクション'):
            # トランザクション開始をシミュレート
            db.set('トランザクション.状態', '開始')
            db.set('トランザクション.変更', [])
            
            print("トランザクション開始")
            
            # 複数の操作をシミュレート
            operations = ['ユーザー作成', '権限設定', 'ログ記録']
            changes = db.get('トランザクション.変更')
            
            for operation in operations:
                changes.append(operation)
                print(f"実行: {operation}")
            
            db.set('トランザクション.変更', changes)
            db.set('トランザクション.状態', '完了')
            
            print(f"トランザクション変更: {db.get('トランザクション.変更')}")
            return True
    
    def simulate_api_request():
        """APIリクエスト処理のシミュレーション"""
        with db.scope('APIリクエスト'):
            db.set('リクエスト.ID', 'req_12345')
            db.set('リクエスト.タイムスタンプ', '2024-06-21T10:00:00Z')
            db.set('リクエスト.ユーザー', 'user_alice')
            
            print(f"API処理開始: {db.get('リクエスト.ID')}")
            
            # ネストしたコンテキストで詳細処理
            with db.scope('認証'):
                db.set('認証.トークン', 'token_xyz')
                db.set('認証.結果', '成功')
                print(f"認証完了: {db.get('認証.結果')}")
            
            # 認証コンテキスト終了後も、リクエストコンテキストは継続
            print(f"認証後のリクエストID: {db.get('リクエスト.ID')}")
            print(f"認証トークン（クリーンアップ済み）: {db.get('認証.トークン')}")
    
    # 各リソース管理を実行
    simulate_database_transaction()
    print("データベーストランザクション完了\n")
    
    simulate_api_request()
    print("APIリクエスト処理完了\n")
    
    # 全てのコンテキストがクリーンアップされたことを確認
    print(f"最終的なスコープ数: {db.scope_count()}")
    print("全てのリソースが適切にクリーンアップされました")
    
    print()


def configuration_contexts():
    """設定コンテキストパターン"""
    print("=== 設定コンテキストパターン ===")
    
    db = EphemeralDB()
    
    # グローバル設定
    db.set('設定.デバッグ', False)
    db.set('設定.ログレベル', 'INFO')
    db.set('設定.データベースURL', 'prod://db')
    
    def run_with_test_config():
        """テスト用設定で実行"""
        with db.scope('テスト設定'):
            # テスト専用設定をオーバーライド
            db.set('設定.デバッグ', True)
            db.set('設定.ログレベル', 'DEBUG')
            db.set('設定.データベースURL', 'test://memory')
            db.set('設定.テストデータ', True)
            
            print("=== テスト環境設定 ===")
            print(f"デバッグ: {db.get('設定.デバッグ')}")
            print(f"ログレベル: {db.get('設定.ログレベル')}")
            print(f"データベースURL: {db.get('設定.データベースURL')}")
            print(f"テストデータ: {db.get('設定.テストデータ')}")
    
    def run_with_dev_config():
        """開発用設定で実行"""
        with db.scope('開発設定'):
            db.set('設定.デバッグ', True)
            db.set('設定.ログレベル', 'DEBUG')
            db.set('設定.開発者ツール', True)
            
            print("=== 開発環境設定 ===")
            print(f"デバッグ: {db.get('設定.デバッグ')}")
            print(f"ログレベル: {db.get('設定.ログレベル')}")
            print(f"データベースURL: {db.get('設定.データベースURL')}")  # 本番環境から継承
            print(f"開発者ツール: {db.get('設定.開発者ツール')}")
    
    # 本番環境設定
    print("=== 本番環境設定 ===")
    print(f"デバッグ: {db.get('設定.デバッグ')}")
    print(f"ログレベル: {db.get('設定.ログレベル')}")
    print(f"データベースURL: {db.get('設定.データベースURL')}")
    print()
    
    # 各環境で実行
    run_with_test_config()
    print()
    
    run_with_dev_config()
    print()
    
    # 本番環境設定に戻る
    print("=== 本番環境設定（復帰後） ===")
    print(f"デバッグ: {db.get('設定.デバッグ')}")
    print(f"ログレベル: {db.get('設定.ログレベル')}")
    print(f"テストデータ: {db.get('設定.テストデータ')}")  # None
    
    print()


if __name__ == "__main__":
    basic_context_manager()
    nested_context_managers()
    exception_handling_in_context()
    resource_management()
    configuration_contexts()
    
    print("=== まとめ ===")
    print("コンテキストマネージャーを使用すると、")
    print("スコープの自動管理と確実なクリーンアップが可能です。")
    print("例外が発生してもリソースは適切に解放されます。")