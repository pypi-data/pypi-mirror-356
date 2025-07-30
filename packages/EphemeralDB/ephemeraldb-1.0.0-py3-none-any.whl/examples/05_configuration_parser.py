#!/usr/bin/env python3
"""
05. 設定パーサー - 階層的な設定管理システム
"""

from ephemeraldb import EphemeralDB
import json
from typing import Dict, Any, List, Optional


class ConfigurationParser:
    """EphemeralDBを使用した階層的設定パーサー"""
    
    def __init__(self):
        self.db = EphemeralDB()
        self.config_stack = []
    
    def load_base_config(self, config: Dict[str, Any]):
        """ベース設定を読み込み"""
        print("=== ベース設定読み込み ===")
        for key, value in config.items():
            self.db.set(key, value)
            print(f"ベース設定: {key} = {value}")
    
    def load_environment_config(self, env_name: str, config: Dict[str, Any]):
        """環境固有の設定を読み込み"""
        with self.db.scope(f'env_{env_name}'):
            print(f"\n=== {env_name}環境設定読み込み ===")
            for key, value in config.items():
                self.db.set(key, value)
                print(f"{env_name}設定: {key} = {value}")
            
            # 現在の有効設定を表示
            self.show_effective_config(env_name)
    
    def load_user_config(self, env_name: str, user_name: str, config: Dict[str, Any]):
        """ユーザー固有の設定を読み込み"""
        with self.db.scope(f'env_{env_name}'):
            with self.db.scope(f'user_{user_name}'):
                print(f"\n=== {env_name}環境の{user_name}ユーザー設定 ===")
                for key, value in config.items():
                    self.db.set(key, value)
                    print(f"{user_name}設定: {key} = {value}")
                
                # 現在の有効設定を表示
                self.show_effective_config(f"{env_name}/{user_name}")
    
    def show_effective_config(self, context: str):
        """現在有効な設定を表示"""
        print(f"\n--- {context}での有効設定 ---")
        
        # 重要な設定項目をチェック
        important_keys = [
            'データベース.ホスト', 'データベース.ポート', 'データベース.名前',
            'API.ベースURL', 'API.タイムアウト', 'API.リトライ回数',
            'ログ.レベル', 'ログ.ファイル',
            'セキュリティ.暗号化', 'セキュリティ.認証',
            'キャッシュ.有効', 'キャッシュ.TTL'
        ]
        
        for key in important_keys:
            value = self.db.get(key)
            if value is not None:
                print(f"  {key}: {value}")
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """設定値を取得（現在のスコープから）"""
        return self.db.get(key, default)
    
    def export_config(self, include_hierarchy: bool = True) -> Dict[str, Any]:
        """現在の設定をエクスポート"""
        return self.db.to_dict(include_hierarchy=include_hierarchy)


def basic_configuration_demo():
    """基本的な設定管理のデモ"""
    print("=== 基本設定管理デモ ===")
    
    parser = ConfigurationParser()
    
    # ベース設定
    base_config = {
        'データベース.ホスト': 'localhost',
        'データベース.ポート': 5432,
        'データベース.名前': 'myapp',
        'API.ベースURL': 'https://api.example.com',
        'API.タイムアウト': 30,
        'API.リトライ回数': 3,
        'ログ.レベル': 'INFO',
        'ログ.ファイル': '/var/log/app.log',
        'セキュリティ.暗号化': True,
        'セキュリティ.認証': 'OAuth2',
        'キャッシュ.有効': True,
        'キャッシュ.TTL': 3600
    }
    
    parser.load_base_config(base_config)
    
    # 開発環境設定
    dev_config = {
        'データベース.ホスト': 'dev-db.local',
        'データベース.名前': 'myapp_dev',
        'API.ベースURL': 'http://localhost:8000',
        'ログ.レベル': 'DEBUG',
        'ログ.ファイル': './dev.log',
        'セキュリティ.暗号化': False,  # 開発環境では無効
    }
    
    parser.load_environment_config('開発', dev_config)
    
    # 本番環境設定
    prod_config = {
        'データベース.ホスト': 'prod-db.cluster.local',
        'データベース.名前': 'myapp_production',
        'API.ベースURL': 'https://api.production.com',
        'API.タイムアウト': 60,  # 本番環境では長めのタイムアウト
        'ログ.レベル': 'WARNING',
        'ログ.ファイル': '/var/log/production/app.log',
        'セキュリティ.認証': 'JWT',  # 本番環境ではJWT
        'キャッシュ.TTL': 7200,  # 本番環境では長めのTTL
    }
    
    parser.load_environment_config('本番', prod_config)
    print()


def user_specific_config_demo():
    """ユーザー固有設定のデモ"""
    print("=== ユーザー固有設定デモ ===")
    
    parser = ConfigurationParser()
    
    # ベース設定
    base_config = {
        'UI.テーマ': '標準',
        'UI.言語': '英語',
        'UI.フォントサイズ': 14,
        '通知.メール': True,
        '通知.プッシュ': True,
        '通知.頻度': 'リアルタイム',
        'プライバシー.分析': True,
        'プライバシー.Cookie': True,
    }
    
    parser.load_base_config(base_config)
    
    # 開発環境でのユーザー設定
    alice_config = {
        'UI.テーマ': 'ダーク',
        'UI.言語': '日本語',
        'UI.フォントサイズ': 16,
        '通知.メール': False,  # アリスはメール通知を無効
        'プライバシー.分析': False,  # プライバシー重視
    }
    
    parser.load_user_config('開発', 'alice', alice_config)
    
    bob_config = {
        'UI.テーマ': 'ライト',
        'UI.フォントサイズ': 12,
        '通知.頻度': '1時間毎',  # ボブは通知頻度を下げる
    }
    
    parser.load_user_config('開発', 'bob', bob_config)
    print()


def nested_config_scopes_demo():
    """ネストした設定スコープのデモ"""
    print("=== ネストした設定スコープデモ ===")
    
    parser = ConfigurationParser()
    
    # グローバル設定
    global_config = {
        'グローバル.会社名': 'テック株式会社',
        'グローバル.バージョン': '1.0.0',
        'グローバル.サポートメール': 'support@tech.co.jp',
        'デフォルト.タイムアウト': 30,
        'デフォルト.リトライ': 3,
        'デフォルト.暗号化': True,
    }
    
    parser.load_base_config(global_config)
    
    # 地域設定（日本）
    with parser.db.scope('地域_日本'):
        region_config = {
            '地域.タイムゾーン': 'Asia/Tokyo',
            '地域.通貨': 'JPY',
            '地域.言語': '日本語',
            '地域.サポート時間': '9:00-18:00 JST',
            'デフォルト.タイムアウト': 45,  # 日本では少し長めに
        }
        
        for key, value in region_config.items():
            parser.db.set(key, value)
        
        print("=== 日本地域設定 ===")
        parser.show_effective_config('日本地域')
        
        # 都市設定（東京）
        with parser.db.scope('都市_東京'):
            city_config = {
                '都市.名前': '東京',
                '都市.データセンター': 'tokyo-1',
                '都市.CDN': 'cloudfront-ap-northeast-1',
                'デフォルト.タイムアウト': 20,  # 東京は高速回線なので短く
            }
            
            for key, value in city_config.items():
                parser.db.set(key, value)
            
            print("\n=== 東京都市設定 ===")
            parser.show_effective_config('日本地域/東京')
            
            # 特定サービス設定
            with parser.db.scope('サービス_支払い'):
                payment_config = {
                    'サービス.名前': '支払いサービス',
                    'サービス.プロバイダー': 'Stripe Japan',
                    'サービス.通貨': 'JPY',
                    'デフォルト.タイムアウト': 60,  # 支払いは慎重に
                    'セキュリティ.レベル': '最高',
                }
                
                for key, value in payment_config.items():
                    parser.db.set(key, value)
                
                print("\n=== 支払いサービス設定 ===")
                parser.show_effective_config('日本地域/東京/支払いサービス')
    
    print()


def configuration_inheritance_demo():
    """設定継承のデモ"""
    print("=== 設定継承デモ ===")
    
    class InheritanceDemo:
        def __init__(self):
            self.db = EphemeralDB()
        
        def test_inheritance_chain(self):
            """継承チェーンのテスト"""
            
            # レベル1: 企業全体の設定
            self.db.set('セキュリティ.ポリシー', '厳格')
            self.db.set('バックアップ.頻度', '毎日')
            self.db.set('ログ.保持期間', 365)
            self.db.set('タイムアウト.デフォルト', 30)
            
            print("企業レベル設定:")
            self._show_current_config(['セキュリティ.ポリシー', 'バックアップ.頻度', 'ログ.保持期間', 'タイムアウト.デフォルト'])
            
            # レベル2: 部門設定
            with self.db.scope('部門_開発'):
                self.db.set('ログ.レベル', 'DEBUG')
                self.db.set('ログ.保持期間', 90)  # 開発部門は短く
                self.db.set('タイムアウト.デフォルト', 60)  # 開発環境は長く
                
                print("\n開発部門設定:")
                self._show_current_config(['セキュリティ.ポリシー', 'バックアップ.頻度', 'ログ.レベル', 'ログ.保持期間', 'タイムアウト.デフォルト'])
                
                # レベル3: チーム設定
                with self.db.scope('チーム_フロントエンド'):
                    self.db.set('ツール.エディタ', 'VSCode')
                    self.db.set('ツール.ブラウザ', 'Chrome')
                    self.db.set('タイムアウト.デフォルト', 10)  # フロントエンドは短く
                    
                    print("\nフロントエンドチーム設定:")
                    self._show_current_config([
                        'セキュリティ.ポリシー', 'バックアップ.頻度', 'ログ.レベル', 
                        'ログ.保持期間', 'タイムアウト.デフォルト', 'ツール.エディタ', 'ツール.ブラウザ'
                    ])
                    
                    # レベル4: 個人設定
                    with self.db.scope('開発者_田中'):
                        self.db.set('個人.テーマ', 'ダーク')
                        self.db.set('個人.フォント', 'Fira Code')
                        self.db.set('ツール.エディタ', 'Neovim')  # 個人的な好み
                        
                        print("\n田中開発者の個人設定:")
                        self._show_current_config([
                            'セキュリティ.ポリシー', 'バックアップ.頻度', 'ログ.レベル', 
                            'ログ.保持期間', 'タイムアウト.デフォルト', 'ツール.エディタ', 
                            'ツール.ブラウザ', '個人.テーマ', '個人.フォント'
                        ])
        
        def _show_current_config(self, keys: List[str]):
            """現在の設定を表示"""
            for key in keys:
                value = self.db.get(key)
                print(f"  {key}: {value}")
    
    demo = InheritanceDemo()
    demo.test_inheritance_chain()
    print()


def configuration_templates_demo():
    """設定テンプレートのデモ"""
    print("=== 設定テンプレートデモ ===")
    
    class ConfigTemplate:
        def __init__(self, name: str):
            self.name = name
            self.db = EphemeralDB()
        
        def apply_template(self, template_name: str, template_config: Dict[str, Any]):
            """テンプレートを適用"""
            with self.db.scope(f'テンプレート_{template_name}'):
                print(f"=== {template_name}テンプレート適用 ===")
                for key, value in template_config.items():
                    self.db.set(key, value)
                    print(f"  {key}: {value}")
                
                return self.get_effective_config()
        
        def get_effective_config(self) -> Dict[str, Any]:
            """有効な設定を取得"""
            return self.db.to_dict(include_hierarchy=True)
    
    # Webアプリケーション用テンプレート
    web_template = {
        'サーバー.ポート': 8080,
        'サーバー.ワーカー数': 4,
        'データベース.接続プール': 10,
        'セッション.タイムアウト': 1800,
        '静的ファイル.キャッシュ': True,
        'ログ.レベル': 'INFO',
        'セキュリティ.HTTPS': True,
        'セキュリティ.CSRF保護': True,
    }
    
    # API用テンプレート
    api_template = {
        'サーバー.ポート': 3000,
        'サーバー.ワーカー数': 8,
        'データベース.接続プール': 20,
        'API.レート制限': 1000,
        'API.CORS': True,
        'ログ.レベル': 'DEBUG',
        'セキュリティ.JWT': True,
        'セキュリティ.API Key': True,
    }
    
    # マイクロサービス用テンプレート
    microservice_template = {
        'サーバー.ポート': 9000,
        'サーバー.ワーカー数': 2,
        'データベース.接続プール': 5,
        'サービス.名前': 'unknown',
        'サービス.バージョン': '1.0.0',
        'ヘルスチェック.間隔': 30,
        'メトリクス.有効': True,
        'トレーシング.有効': True,
    }
    
    # 各テンプレートをテスト
    config = ConfigTemplate('テストアプリ')
    
    # ベース設定
    base_config = {
        'アプリ.名前': 'サンプルアプリ',
        'アプリ.バージョン': '2.0.0',
        'ログ.ファイル': '/var/log/app.log',
    }
    
    for key, value in base_config.items():
        config.db.set(key, value)
    
    print("ベース設定:")
    print(json.dumps(config.get_effective_config(), indent=2, ensure_ascii=False))
    
    # Webテンプレート適用
    web_config = config.apply_template('Web', web_template)
    print("\nWebテンプレート適用後:")
    print(json.dumps(web_config, indent=2, ensure_ascii=False))
    
    # APIテンプレート適用（新しいスコープ）
    api_config = config.apply_template('API', api_template)
    print("\nAPIテンプレート適用後:")
    print(json.dumps(api_config, indent=2, ensure_ascii=False))
    
    print()


if __name__ == "__main__":
    basic_configuration_demo()
    user_specific_config_demo()
    nested_config_scopes_demo()
    configuration_inheritance_demo()
    configuration_templates_demo()
    
    print("=== まとめ ===")
    print("EphemeralDBを使用することで、複雑な階層構造を持つ")
    print("設定管理システムを簡単に実装できます。")
    print("環境、ユーザー、地域などの様々な条件に応じた")
    print("設定の継承と上書きが自然に表現できます。")