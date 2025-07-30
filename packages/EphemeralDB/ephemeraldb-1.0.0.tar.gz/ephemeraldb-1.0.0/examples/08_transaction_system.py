#!/usr/bin/env python3
"""
08. トランザクションシステム - ネストしたトランザクション処理
"""

from ephemeraldb import EphemeralDB
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import uuid
import time
from contextlib import contextmanager


class TransactionStatus(Enum):
    """トランザクション状態"""
    ACTIVE = "アクティブ"
    COMMITTED = "コミット済み"
    ABORTED = "中止"
    PREPARED = "準備完了"


class IsolationLevel(Enum):
    """分離レベル"""
    READ_UNCOMMITTED = "READ_UNCOMMITTED"
    READ_COMMITTED = "READ_COMMITTED"
    REPEATABLE_READ = "REPEATABLE_READ"
    SERIALIZABLE = "SERIALIZABLE"


class TransactionManager:
    """EphemeralDBを使用したトランザクション管理システム"""
    
    def __init__(self):
        self.db = EphemeralDB()
        self.active_transactions = {}
        self.transaction_stack = []
        
        # グローバルデータ領域の初期化
        self.db.set('グローバルデータ', {})
        self.db.set('ロック情報', {})
        self.db.set('トランザクション履歴', [])
    
    @contextmanager
    def transaction(self, name: Optional[str] = None, isolation_level: IsolationLevel = IsolationLevel.READ_COMMITTED):
        """トランザクションコンテキストマネージャー"""
        tx_id = str(uuid.uuid4())[:8]
        tx_name = name or f"TX_{tx_id}"
        
        # トランザクション開始
        self.begin_transaction(tx_id, tx_name, isolation_level)
        
        try:
            yield tx_id
            # 正常終了時はコミット
            self.commit_transaction(tx_id)
        except Exception as e:
            # 例外発生時はロールバック
            print(f"トランザクション例外: {e}")
            self.rollback_transaction(tx_id)
            raise
    
    def begin_transaction(self, tx_id: str, name: str, isolation_level: IsolationLevel):
        """トランザクション開始"""
        with self.db.scope(f'トランザクション_{tx_id}'):
            print(f"[{tx_id}] トランザクション開始: {name}")
            
            # トランザクション情報を設定
            self.db.set('トランザクションID', tx_id)
            self.db.set('トランザクション名', name)
            self.db.set('状態', TransactionStatus.ACTIVE)
            self.db.set('分離レベル', isolation_level)
            self.db.set('開始時刻', time.time())
            self.db.set('変更ログ', [])
            self.db.set('読み取りセット', set())
            self.db.set('書き込みセット', set())
            
            # アクティブトランザクションに登録
            self.active_transactions[tx_id] = {
                'name': name,
                'scope_count': self.db.scope_count(),
                'isolation_level': isolation_level
            }
            
            # トランザクションスタックにプッシュ
            self.transaction_stack.append(tx_id)
    
    def commit_transaction(self, tx_id: str):
        """トランザクションコミット"""
        if tx_id not in self.active_transactions:
            raise ValueError(f"アクティブでないトランザクション: {tx_id}")
        
        with self.db.scope(f'トランザクション_{tx_id}'):
            print(f"[{tx_id}] トランザクションコミット開始")
            
            # 変更ログを取得
            change_log = self.db.get('変更ログ', [])
            
            # 変更をグローバルデータに適用
            global_data = self.db.get('グローバルデータ')
            
            for change in change_log:
                if change['操作'] == 'SET':
                    self._set_global_data(global_data, change['キー'], change['新しい値'])
                elif change['操作'] == 'DELETE':
                    self._delete_global_data(global_data, change['キー'])
            
            self.db.set('グローバルデータ', global_data)
            
            # 状態を更新
            self.db.set('状態', TransactionStatus.COMMITTED)
            self.db.set('コミット時刻', time.time())
            
            # トランザクション履歴に記録
            history = self.db.get('トランザクション履歴')
            history.append({
                'トランザクションID': tx_id,
                '名前': self.db.get('トランザクション名'),
                '状態': TransactionStatus.COMMITTED.value,
                '開始時刻': self.db.get('開始時刻'),
                'コミット時刻': time.time(),
                '変更数': len(change_log)
            })
            self.db.set('トランザクション履歴', history)
            
            print(f"[{tx_id}] コミット完了 ({len(change_log)}件の変更)")
        
        # クリーンアップ
        self._cleanup_transaction(tx_id)
    
    def rollback_transaction(self, tx_id: str):
        """トランザクションロールバック"""
        if tx_id not in self.active_transactions:
            print(f"警告: アクティブでないトランザクション: {tx_id}")
            return
        
        with self.db.scope(f'トランザクション_{tx_id}'):
            print(f"[{tx_id}] トランザクションロールバック")
            
            # 状態を更新
            self.db.set('状態', TransactionStatus.ABORTED)
            self.db.set('ロールバック時刻', time.time())
            
            # 変更ログを取得（ログのみ、実際の変更は適用しない）
            change_log = self.db.get('変更ログ', [])
            
            # トランザクション履歴に記録
            history = self.db.get('トランザクション履歴')
            history.append({
                'トランザクションID': tx_id,
                '名前': self.db.get('トランザクション名'),
                '状態': TransactionStatus.ABORTED.value,
                '開始時刻': self.db.get('開始時刻'),
                'ロールバック時刻': time.time(),
                '変更数': len(change_log)
            })
            self.db.set('トランザクション履歴', history)
            
            print(f"[{tx_id}] ロールバック完了 ({len(change_log)}件の変更を破棄)")
        
        # クリーンアップ
        self._cleanup_transaction(tx_id)
    
    def set_data(self, tx_id: str, key: str, value: Any):
        """トランザクション内でデータ設定"""
        with self.db.scope(f'トランザクション_{tx_id}'):
            # 現在の値を取得（変更ログ用）
            current_value = self.get_data(tx_id, key)
            
            # 変更ログに記録
            change_log = self.db.get('変更ログ')
            change_log.append({
                '操作': 'SET',
                'キー': key,
                '古い値': current_value,
                '新しい値': value,
                '時刻': time.time()
            })
            self.db.set('変更ログ', change_log)
            
            # 書き込みセットに追加
            write_set = self.db.get('書き込みセット')
            write_set.add(key)
            self.db.set('書き込みセット', write_set)
            
            # トランザクション内の一時データとして保存
            self.db.set(f'データ.{key}', value)
            
            print(f"[{tx_id}] SET {key} = {value}")
    
    def get_data(self, tx_id: str, key: str, default: Any = None) -> Any:
        """トランザクション内でデータ取得"""
        with self.db.scope(f'トランザクション_{tx_id}'):
            # 読み取りセットに追加
            read_set = self.db.get('読み取りセット')
            read_set.add(key)
            self.db.set('読み取りセット', read_set)
            
            # まずトランザクション内の変更をチェック
            tx_value = self.db.get(f'データ.{key}')
            if tx_value is not None:
                return tx_value
            
            # グローバルデータから取得
            global_data = self.db.get('グローバルデータ')
            value = self._get_global_data(global_data, key, default)
            
            print(f"[{tx_id}] GET {key} => {value}")
            return value
    
    def delete_data(self, tx_id: str, key: str):
        """トランザクション内でデータ削除"""
        with self.db.scope(f'トランザクション_{tx_id}'):
            # 現在の値を取得（変更ログ用）
            current_value = self.get_data(tx_id, key)
            
            # 変更ログに記録
            change_log = self.db.get('変更ログ')
            change_log.append({
                '操作': 'DELETE',
                'キー': key,
                '古い値': current_value,
                '時刻': time.time()
            })
            self.db.set('変更ログ', change_log)
            
            # 書き込みセットに追加
            write_set = self.db.get('書き込みセット')
            write_set.add(key)
            self.db.set('書き込みセット', write_set)
            
            # トランザクション内で削除マーク
            self.db.set(f'データ.{key}', '__DELETED__')
            
            print(f"[{tx_id}] DELETE {key}")
    
    def _set_global_data(self, global_data: Dict, key: str, value: Any):
        """グローバルデータに値を設定（ドット記法対応）"""
        keys = key.split('.')
        current = global_data
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def _get_global_data(self, global_data: Dict, key: str, default: Any = None) -> Any:
        """グローバルデータから値を取得（ドット記法対応）"""
        keys = key.split('.')
        current = global_data
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def _delete_global_data(self, global_data: Dict, key: str):
        """グローバルデータから値を削除（ドット記法対応）"""
        keys = key.split('.')
        current = global_data
        
        try:
            for k in keys[:-1]:
                current = current[k]
            if keys[-1] in current:
                del current[keys[-1]]
        except (KeyError, TypeError):
            pass
    
    def _cleanup_transaction(self, tx_id: str):
        """トランザクションクリーンアップ"""
        if tx_id in self.active_transactions:
            del self.active_transactions[tx_id]
        
        if tx_id in self.transaction_stack:
            self.transaction_stack.remove(tx_id)
    
    def get_transaction_status(self, tx_id: str) -> Optional[TransactionStatus]:
        """トランザクション状態取得"""
        if tx_id not in self.active_transactions:
            return None
        
        with self.db.scope(f'トランザクション_{tx_id}'):
            return self.db.get('状態')
    
    def get_active_transactions(self) -> List[str]:
        """アクティブなトランザクション一覧"""
        return list(self.active_transactions.keys())
    
    def get_transaction_history(self) -> List[Dict[str, Any]]:
        """トランザクション履歴取得"""
        return self.db.get('トランザクション履歴', [])


def basic_transaction_demo():
    """基本的なトランザクション機能のデモ"""
    print("=== 基本トランザクション機能 ===")
    
    tm = TransactionManager()
    
    # 初期データ設定
    with tm.transaction("初期データ設定") as tx_id:
        tm.set_data(tx_id, 'アカウント.Alice.残高', 1000)
        tm.set_data(tx_id, 'アカウント.Bob.残高', 500)
        tm.set_data(tx_id, 'アカウント.Charlie.残高', 750)
    
    print("初期データ設定完了")
    
    # 正常なトランザクション
    with tm.transaction("正常な送金") as tx_id:
        alice_balance = tm.get_data(tx_id, 'アカウント.Alice.残高')
        bob_balance = tm.get_data(tx_id, 'アカウント.Bob.残高')
        
        print(f"送金前 - Alice: {alice_balance}円, Bob: {bob_balance}円")
        
        # Alice から Bob に 200円送金
        transfer_amount = 200
        if alice_balance >= transfer_amount:
            tm.set_data(tx_id, 'アカウント.Alice.残高', alice_balance - transfer_amount)
            tm.set_data(tx_id, 'アカウント.Bob.残高', bob_balance + transfer_amount)
            
            new_alice = tm.get_data(tx_id, 'アカウント.Alice.残高')
            new_bob = tm.get_data(tx_id, 'アカウント.Bob.残高')
            print(f"送金後 - Alice: {new_alice}円, Bob: {new_bob}円")
    
    # 失敗するトランザクション（例外による自動ロールバック）
    try:
        with tm.transaction("失敗する送金") as tx_id:
            alice_balance = tm.get_data(tx_id, 'アカウント.Alice.残高')
            charlie_balance = tm.get_data(tx_id, 'アカウント.Charlie.残高')
            
            print(f"失敗送金前 - Alice: {alice_balance}円, Charlie: {charlie_balance}円")
            
            # Alice から Charlie に 2000円送金（残高不足）
            transfer_amount = 2000
            if alice_balance < transfer_amount:
                raise ValueError(f"残高不足: 必要{transfer_amount}円, 残高{alice_balance}円")
            
            tm.set_data(tx_id, 'アカウント.Alice.残高', alice_balance - transfer_amount)
            tm.set_data(tx_id, 'アカウント.Charlie.残高', charlie_balance + transfer_amount)
    
    except ValueError as e:
        print(f"送金失敗: {e}")
    
    # 最終残高確認（失敗したトランザクションは反映されない）
    with tm.transaction("残高確認") as tx_id:
        alice_final = tm.get_data(tx_id, 'アカウント.Alice.残高')
        bob_final = tm.get_data(tx_id, 'アカウント.Bob.残高')
        charlie_final = tm.get_data(tx_id, 'アカウント.Charlie.残高')
        
        print(f"最終残高 - Alice: {alice_final}円, Bob: {bob_final}円, Charlie: {charlie_final}円")
    
    print()


def nested_transaction_demo():
    """ネストしたトランザクションのデモ"""
    print("=== ネストしたトランザクション ===")
    
    tm = TransactionManager()
    
    # 複合的な業務処理のシミュレーション
    with tm.transaction("注文処理") as outer_tx:
        # 注文情報設定
        tm.set_data(outer_tx, '注文.ID', 'ORDER_001')
        tm.set_data(outer_tx, '注文.顧客', 'Alice')
        tm.set_data(outer_tx, '注文.商品', [{'商品ID': 'P001', '数量': 2, '単価': 500}])
        
        print("注文情報を設定しました")
        
        # 在庫チェックと更新（ネストしたトランザクション）
        try:
            with tm.transaction("在庫処理") as stock_tx:
                current_stock = tm.get_data(stock_tx, '在庫.P001', 10)
                required_qty = 2
                
                print(f"在庫チェック - 商品P001: 現在{current_stock}個, 必要{required_qty}個")
                
                if current_stock >= required_qty:
                    new_stock = current_stock - required_qty
                    tm.set_data(stock_tx, '在庫.P001', new_stock)
                    tm.set_data(stock_tx, '注文.在庫確保', True)
                    print(f"在庫を{required_qty}個確保。残り{new_stock}個")
                else:
                    raise ValueError("在庫不足")
        
        except ValueError as e:
            print(f"在庫処理失敗: {e}")
            # 外側のトランザクションも失敗させる
            raise
        
        # 決済処理（別のネストしたトランザクション）
        try:
            with tm.transaction("決済処理") as payment_tx:
                customer_balance = tm.get_data(payment_tx, 'アカウント.Alice.残高', 0)
                order_total = 1000  # 2 * 500円
                
                print(f"決済処理 - 顧客残高: {customer_balance}円, 注文金額: {order_total}円")
                
                if customer_balance >= order_total:
                    new_balance = customer_balance - order_total
                    tm.set_data(payment_tx, 'アカウント.Alice.残高', new_balance)
                    tm.set_data(payment_tx, '注文.決済完了', True)
                    tm.set_data(payment_tx, '注文.決済金額', order_total)
                    print(f"決済完了。残高: {new_balance}円")
                else:
                    raise ValueError("残高不足")
        
        except ValueError as e:
            print(f"決済処理失敗: {e}")
            raise
        
        # 注文完了
        tm.set_data(outer_tx, '注文.状態', '完了')
        tm.set_data(outer_tx, '注文.完了時刻', time.time())
        
        print("注文処理が正常に完了しました")
    
    print()


def concurrent_transaction_simulation():
    """同時実行トランザクションのシミュレーション"""
    print("=== 同時実行トランザクションシミュレーション ===")
    
    tm = TransactionManager()
    
    # 初期データ
    with tm.transaction("初期設定") as tx_id:
        tm.set_data(tx_id, '共有リソース.カウンター', 0)
        tm.set_data(tx_id, '共有リソース.合計', 0)
    
    # 複数のトランザクションを順次実行（実際の同時実行ではなく、概念的なデモ）
    transactions = []
    
    # トランザクション1: カウンターを増加
    print("トランザクション1開始（カウンター増加）")
    tm.begin_transaction("TX1", "カウンター増加", IsolationLevel.READ_COMMITTED)
    
    with tm.db.scope('トランザクション_TX1'):
        current_counter = tm.get_data("TX1", '共有リソース.カウンター')
        print(f"TX1: 現在のカウンター = {current_counter}")
        tm.set_data("TX1", '共有リソース.カウンター', current_counter + 1)
        
        # まだコミットしない（他のトランザクションの動作を確認するため）
        print("TX1: カウンターを+1（未コミット）")
    
    # トランザクション2: 合計を更新
    print("トランザクション2開始（合計更新）")
    tm.begin_transaction("TX2", "合計更新", IsolationLevel.READ_COMMITTED)
    
    with tm.db.scope('トランザクション_TX2'):
        # TX1の変更はまだコミットされていないので見えない
        current_counter = tm.get_data("TX2", '共有リソース.カウンター')
        current_total = tm.get_data("TX2", '共有リソース.合計')
        
        print(f"TX2: カウンター = {current_counter}, 合計 = {current_total}")
        new_total = current_total + current_counter * 10
        tm.set_data("TX2", '共有リソース.合計', new_total)
        print(f"TX2: 合計を{new_total}に更新")
    
    # TX2をコミット
    tm.commit_transaction("TX2")
    
    # TX1をコミット
    tm.commit_transaction("TX1")
    
    # 最終状態確認
    with tm.transaction("最終確認") as tx_id:
        final_counter = tm.get_data(tx_id, '共有リソース.カウンター')
        final_total = tm.get_data(tx_id, '共有リソース.合計')
        print(f"最終状態 - カウンター: {final_counter}, 合計: {final_total}")
    
    print()


def transaction_history_demo():
    """トランザクション履歴のデモ"""
    print("=== トランザクション履歴 ===")
    
    tm = TransactionManager()
    
    # 複数のトランザクションを実行
    with tm.transaction("ユーザー登録") as tx_id:
        tm.set_data(tx_id, 'ユーザー.user001.名前', '田中太郎')
        tm.set_data(tx_id, 'ユーザー.user001.メール', 'tanaka@example.com')
        tm.set_data(tx_id, 'ユーザー.user001.登録日', time.time())
    
    try:
        with tm.transaction("無効なデータ更新") as tx_id:
            tm.set_data(tx_id, 'ユーザー.user001.名前', '')  # 空の名前
            raise ValueError("名前が空です")
    except ValueError:
        pass  # ロールバックされる
    
    with tm.transaction("プロフィール更新") as tx_id:
        tm.set_data(tx_id, 'ユーザー.user001.プロフィール.年齢', 30)
        tm.set_data(tx_id, 'ユーザー.user001.プロフィール.職業', 'エンジニア')
    
    # 履歴表示
    history = tm.get_transaction_history()
    print("トランザクション履歴:")
    for i, tx_record in enumerate(history, 1):
        print(f"  {i}. {tx_record['名前']} - {tx_record['状態']} ({tx_record['変更数']}件の変更)")
    
    # 最終データ確認
    with tm.transaction("データ確認") as tx_id:
        user_name = tm.get_data(tx_id, 'ユーザー.user001.名前')
        user_email = tm.get_data(tx_id, 'ユーザー.user001.メール')
        user_age = tm.get_data(tx_id, 'ユーザー.user001.プロフィール.年齢')
        user_job = tm.get_data(tx_id, 'ユーザー.user001.プロフィール.職業')
        
        print(f"\n最終データ:")
        print(f"  名前: {user_name}")
        print(f"  メール: {user_email}")
        print(f"  年齢: {user_age}")
        print(f"  職業: {user_job}")
    
    print()


if __name__ == "__main__":
    basic_transaction_demo()
    nested_transaction_demo()
    concurrent_transaction_simulation()
    transaction_history_demo()
    
    print("=== まとめ ===")
    print("EphemeralDBを使用することで、本格的なトランザクション")
    print("システムを実装できます。ネストしたトランザクション、")
    print("自動ロールバック、分離レベルなどの高度な機能も")
    print("スコープ管理により自然に表現できます。")