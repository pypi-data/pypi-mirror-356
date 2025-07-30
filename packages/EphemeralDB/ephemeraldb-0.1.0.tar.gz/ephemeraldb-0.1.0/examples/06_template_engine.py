#!/usr/bin/env python3
"""
06. テンプレートエンジン - 変数スコープを持つテンプレート処理
"""

from ephemeraldb import EphemeralDB
import re
from typing import Dict, Any, List, Optional


class SimpleTemplateEngine:
    """EphemeralDBを使用したシンプルなテンプレートエンジン"""
    
    def __init__(self):
        self.db = EphemeralDB()
        self.includes = {}  # インクルードされるテンプレート
        self.filters = {
            'upper': str.upper,
            'lower': str.lower,
            'title': str.title,
            'length': len,
            'reverse': lambda x: x[::-1] if isinstance(x, str) else str(x)[::-1],
        }
    
    def set_global_variable(self, key: str, value: Any):
        """グローバル変数を設定"""
        self.db.set(key, value)
    
    def register_include(self, name: str, template: str):
        """インクルード用テンプレートを登録"""
        self.includes[name] = template
    
    def render(self, template: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """テンプレートをレンダリング"""
        with self.db.scope('レンダリング'):
            # ローカル変数を設定
            if variables:
                for key, value in variables.items():
                    self.db.set(key, value)
            
            # テンプレートを処理
            return self._process_template(template)
    
    def render_with_layout(self, layout: str, content: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """レイアウト付きレンダリング"""
        with self.db.scope('レイアウト'):
            # コンテンツを変数として設定
            self.db.set('content', content)
            
            if variables:
                for key, value in variables.items():
                    self.db.set(key, value)
            
            return self._process_template(layout)
    
    def _process_template(self, template: str) -> str:
        """テンプレートを処理"""
        result = template
        
        # 1. インクルード処理 {{ include "template_name" }}
        result = self._process_includes(result)
        
        # 2. 変数置換 {{ variable_name }}
        result = self._process_variables(result)
        
        # 3. フィルター処理 {{ variable_name | filter }}
        result = self._process_filters(result)
        
        # 4. 条件分岐 {% if condition %} ... {% endif %}
        result = self._process_conditionals(result)
        
        # 5. ループ処理 {% for item in list %} ... {% endfor %}
        result = self._process_loops(result)
        
        return result
    
    def _process_includes(self, template: str) -> str:
        """インクルード処理"""
        include_pattern = r'\{\{\s*include\s+"([^"]+)"\s*\}\}'
        
        def replace_include(match):
            include_name = match.group(1)
            if include_name in self.includes:
                # インクルードを新しいスコープで処理
                with self.db.scope(f'インクルード_{include_name}'):
                    return self._process_template(self.includes[include_name])
            return f"[ERROR: インクルード '{include_name}' が見つかりません]"
        
        return re.sub(include_pattern, replace_include, template)
    
    def _process_variables(self, template: str) -> str:
        """変数置換処理"""
        var_pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}'
        
        def replace_var(match):
            var_name = match.group(1)
            value = self.db.get(var_name)
            return str(value) if value is not None else f"[UNDEFINED: {var_name}]"
        
        return re.sub(var_pattern, replace_var, template)
    
    def _process_filters(self, template: str) -> str:
        """フィルター処理"""
        filter_pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\|\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}'
        
        def apply_filter(match):
            var_name = match.group(1)
            filter_name = match.group(2)
            
            value = self.db.get(var_name)
            if value is None:
                return f"[UNDEFINED: {var_name}]"
            
            if filter_name in self.filters:
                try:
                    filtered_value = self.filters[filter_name](value)
                    return str(filtered_value)
                except Exception as e:
                    return f"[FILTER ERROR: {filter_name} - {e}]"
            else:
                return f"[UNKNOWN FILTER: {filter_name}]"
        
        return re.sub(filter_pattern, apply_filter, template)
    
    def _process_conditionals(self, template: str) -> str:
        """条件分岐処理"""
        if_pattern = r'\{%\s*if\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s*%\}(.*?)\{%\s*endif\s*%\}'
        
        def process_if(match):
            var_name = match.group(1)
            content = match.group(2)
            
            value = self.db.get(var_name)
            if value:  # Truthy check
                return self._process_template(content)
            else:
                return ""
        
        return re.sub(if_pattern, process_if, template, flags=re.DOTALL)
    
    def _process_loops(self, template: str) -> str:
        """ループ処理"""
        for_pattern = r'\{%\s*for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s*%\}(.*?)\{%\s*endfor\s*%\}'
        
        def process_for(match):
            item_var = match.group(1)
            list_var = match.group(2)
            content = match.group(3)
            
            items = self.db.get(list_var)
            if not isinstance(items, (list, tuple)):
                return f"[ERROR: {list_var} はリストではありません]"
            
            result = []
            for i, item in enumerate(items):
                # 各アイテムを新しいスコープで処理
                with self.db.scope(f'ループ_{i}'):
                    self.db.set(item_var, item)
                    self.db.set('loop_index', i)
                    self.db.set('loop_first', i == 0)
                    self.db.set('loop_last', i == len(items) - 1)
                    result.append(self._process_template(content))
            
            return ''.join(result)
        
        return re.sub(for_pattern, process_for, template, flags=re.DOTALL)


def basic_template_demo():
    """基本的なテンプレート機能のデモ"""
    print("=== 基本テンプレート機能 ===")
    
    engine = SimpleTemplateEngine()
    
    # グローバル変数設定
    engine.set_global_variable('サイト名', 'マイウェブサイト')
    engine.set_global_variable('年', 2024)
    
    # 基本的な変数置換
    template1 = """
こんにちは、{{ ユーザー名 }}さん！
{{ サイト名 }}へようこそ。
今年は{{ 年 }}年です。
"""
    
    result1 = engine.render(template1, {
        'ユーザー名': 'アリス'
    })
    
    print("基本テンプレート結果:")
    print(result1)


def filter_demo():
    """フィルター機能のデモ"""
    print("=== フィルター機能 ===")
    
    engine = SimpleTemplateEngine()
    
    template = """
元の名前: {{ 名前 }}
大文字: {{ 名前 | upper }}
小文字: {{ 名前 | lower }}
タイトルケース: {{ 名前 | title }}
逆順: {{ 名前 | reverse }}
文字数: {{ 名前 | length }}
"""
    
    result = engine.render(template, {
        '名前': 'Hello World'
    })
    
    print("フィルター結果:")
    print(result)


def conditional_demo():
    """条件分岐のデモ"""
    print("=== 条件分岐 ===")
    
    engine = SimpleTemplateEngine()
    
    template = """
ユーザー: {{ ユーザー名 }}
{% if 管理者 %}
管理者権限があります。
管理者メニューを表示します。
{% endif %}
{% if プレミアム %}
プレミアム機能が利用可能です。
{% endif %}
"""
    
    # 管理者ユーザー
    result1 = engine.render(template, {
        'ユーザー名': 'admin',
        '管理者': True,
        'プレミアム': False
    })
    
    print("管理者ユーザー:")
    print(result1)
    
    # 一般ユーザー
    result2 = engine.render(template, {
        'ユーザー名': 'user',
        '管理者': False,
        'プレミアム': True
    })
    
    print("一般ユーザー:")
    print(result2)


def loop_demo():
    """ループ処理のデモ"""
    print("=== ループ処理 ===")
    
    engine = SimpleTemplateEngine()
    
    template = """
商品一覧:
{% for 商品 in 商品リスト %}
  {{ loop_index }}. {{ 商品.名前 }} - ¥{{ 商品.価格 }}
  {% if loop_first %}(新着商品){% endif %}
  {% if loop_last %}(最後の商品){% endif %}
{% endfor %}

合計: {{ 商品リスト | length }}件
"""
    
    result = engine.render(template, {
        '商品リスト': [
            {'名前': 'ノートPC', '価格': 89800},
            {'名前': 'マウス', '価格': 2980},
            {'名前': 'キーボード', '価格': 8900},
        ]
    })
    
    print("ループ結果:")
    print(result)


def include_demo():
    """インクルード機能のデモ"""
    print("=== インクルード機能 ===")
    
    engine = SimpleTemplateEngine()
    
    # インクルード用テンプレート登録
    engine.register_include('ヘッダー', """
=== {{ サイト名 }} ===
ナビゲーション: ホーム | 商品 | お問い合わせ
""")
    
    engine.register_include('フッター', """
---
© {{ 年 }} {{ サイト名 }}. All rights reserved.
お問い合わせ: {{ 連絡先 }}
---
""")
    
    # メインテンプレート
    main_template = """
{{ include "ヘッダー" }}

メインコンテンツ:
こんにちは、{{ ユーザー名 }}さん！
今日の特別オファーをご覧ください。

{{ include "フッター" }}
"""
    
    engine.set_global_variable('サイト名', 'Eコマースサイト')
    engine.set_global_variable('年', 2024)
    engine.set_global_variable('連絡先', 'support@example.com')
    
    result = engine.render(main_template, {
        'ユーザー名': 'ボブ'
    })
    
    print("インクルード結果:")
    print(result)


def layout_demo():
    """レイアウト機能のデモ"""
    print("=== レイアウト機能 ===")
    
    engine = SimpleTemplateEngine()
    
    # レイアウトテンプレート
    layout = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ タイトル }} - {{ サイト名 }}</title>
</head>
<body>
    <header>
        <h1>{{ サイト名 }}</h1>
        <nav>ホーム | {{ セクション }}</nav>
    </header>
    
    <main>
{{ content }}
    </main>
    
    <footer>
        <p>© {{ 年 }} {{ サイト名 }}</p>
    </footer>
</body>
</html>
"""
    
    # コンテンツ
    content = """
        <h2>{{ ページタイトル }}</h2>
        <p>{{ メッセージ }}</p>
        
        <ul>
        {% for アイテム in リスト %}
            <li>{{ アイテム }}</li>
        {% endfor %}
        </ul>
"""
    
    engine.set_global_variable('サイト名', 'ブログサイト')
    engine.set_global_variable('年', 2024)
    
    result = engine.render_with_layout(layout, content, {
        'タイトル': 'ホームページ',
        'セクション': 'ブログ',
        'ページタイトル': '最新記事',
        'メッセージ': 'EphemeralDBの活用例をご紹介します。',
        'リスト': ['スコープ管理', 'テンプレート処理', '設定管理']
    })
    
    print("レイアウト結果:")
    print(result)


def nested_scopes_demo():
    """ネストしたスコープでの変数管理"""
    print("=== ネストしたスコープでの変数管理 ===")
    
    engine = SimpleTemplateEngine()
    
    # 複雑なネスト構造のテンプレート
    engine.register_include('商品カード', """
    <div class="商品カード">
        <h3>{{ 商品.名前 }}</h3>
        <p>価格: ¥{{ 商品.価格 }}</p>
        {% if 割引率 %}
        <p class="割引">{{ 割引率 }}%オフ！</p>
        {% endif %}
        <p>カテゴリ: {{ カテゴリ名 }}</p>
    </div>
""")
    
    main_template = """
<div class="ショップ">
    <h1>{{ ショップ名 }}</h1>
    
    {% for カテゴリ in カテゴリリスト %}
    <section class="カテゴリ">
        <h2>{{ カテゴリ.名前 }}</h2>
        
        {% for 商品 in カテゴリ.商品 %}
            {{ include "商品カード" }}
        {% endfor %}
    </section>
    {% endfor %}
</div>
"""
    
    # グローバル変数（すべてのスコープからアクセス可能）
    engine.set_global_variable('ショップ名', 'テックストア')
    engine.set_global_variable('割引率', 10)
    
    result = engine.render(main_template, {
        'カテゴリリスト': [
            {
                '名前': 'コンピューター',
                '商品': [
                    {'名前': 'ノートPC', '価格': 89800},
                    {'名前': 'デスクトップPC', '価格': 129800},
                ]
            },
            {
                '名前': '周辺機器', 
                '商品': [
                    {'名前': 'マウス', '価格': 2980},
                    {'名前': 'キーボード', '価格': 8900},
                ]
            }
        ]
    })
    
    print("ネストしたスコープ結果:")
    print(result)


def template_inheritance_demo():
    """テンプレート継承のシミュレーション"""
    print("=== テンプレート継承シミュレーション ===")
    
    class InheritanceEngine(SimpleTemplateEngine):
        """継承機能付きテンプレートエンジン"""
        
        def render_with_inheritance(self, child_template: str, parent_template: str, variables: Optional[Dict[str, Any]] = None) -> str:
            """親テンプレートを継承してレンダリング"""
            with self.db.scope('継承'):
                # 子テンプレートの変数を設定
                if variables:
                    for key, value in variables.items():
                        self.db.set(key, value)
                
                # 子テンプレートで定義されたブロックを抽出
                blocks = self._extract_blocks(child_template)
                
                # ブロックを変数として設定
                for block_name, block_content in blocks.items():
                    with self.db.scope(f'ブロック_{block_name}'):
                        processed_content = self._process_template(block_content)
                        self.db.set(f'ブロック_{block_name}', processed_content)
                
                # 親テンプレートをレンダリング
                return self._process_template(parent_template)
        
        def _extract_blocks(self, template: str) -> Dict[str, str]:
            """ブロックを抽出"""
            block_pattern = r'\{%\s*block\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*%\}(.*?)\{%\s*endblock\s*%\}'
            blocks = {}
            
            for match in re.finditer(block_pattern, template, re.DOTALL):
                block_name = match.group(1)
                block_content = match.group(2).strip()
                blocks[block_name] = block_content
            
            return blocks
    
    engine = InheritanceEngine()
    
    # 基本レイアウト（親テンプレート）
    base_layout = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ ブロック_title }}</title>
    <style>{{ ブロック_styles }}</style>
</head>
<body>
    <header>
        <h1>{{ サイト名 }}</h1>
    </header>
    
    <main>
{{ ブロック_content }}
    </main>
    
    <footer>
        {{ ブロック_footer }}
    </footer>
    
    <script>{{ ブロック_scripts }}</script>
</body>
</html>
"""
    
    # 子テンプレート
    child_template = """
{% block title %}{{ ページタイトル }} - ブログ{% endblock %}

{% block styles %}
body { font-family: Arial; }
.記事 { margin: 20px; }
{% endblock %}

{% block content %}
<article class="記事">
    <h2>{{ 記事タイトル }}</h2>
    <p>投稿者: {{ 投稿者 }}</p>
    <div>{{ 記事内容 }}</div>
</article>
{% endblock %}

{% block footer %}
<p>© 2024 {{ サイト名 }} - すべての権利を保有</p>
{% endblock %}

{% block scripts %}
console.log('ページが読み込まれました');
{% endblock %}
"""
    
    engine.set_global_variable('サイト名', 'テックブログ')
    
    result = engine.render_with_inheritance(child_template, base_layout, {
        'ページタイトル': 'EphemeralDB入門',
        '記事タイトル': 'EphemeralDBの基本的な使い方',
        '投稿者': '田中太郎',
        '記事内容': 'EphemeralDBは軽量で使いやすいメモリストレージです...'
    })
    
    print("テンプレート継承結果:")
    print(result)


if __name__ == "__main__":
    basic_template_demo()
    print()
    
    filter_demo()
    print()
    
    conditional_demo()
    print()
    
    loop_demo()
    print()
    
    include_demo()
    print()
    
    layout_demo()
    print()
    
    nested_scopes_demo()
    print()
    
    template_inheritance_demo()
    
    print("\n=== まとめ ===")
    print("EphemeralDBを使用したテンプレートエンジンにより、")
    print("変数スコープを適切に管理しながら複雑なテンプレート処理が可能です。")
    print("インクルード、レイアウト、継承などの高度な機能も実現できます。")