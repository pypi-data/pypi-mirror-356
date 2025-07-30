#!/usr/bin/env python3
"""
07. ステートマシン - 状態遷移を管理するステートマシンの実装
"""

from ephemeraldb import EphemeralDB
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import time


class TransitionResult(Enum):
    """遷移結果"""
    SUCCESS = "成功"
    FAILED = "失敗"
    FORBIDDEN = "禁止"
    ERROR = "エラー"


class StateMachine:
    """EphemeralDBを使用したステートマシン"""
    
    def __init__(self, name: str):
        self.name = name
        self.db = EphemeralDB()
        self.states = {}
        self.transitions = {}
        self.guards = {}
        self.actions = {}
        self.current_state = None
        
        # 初期化
        self.db.set('マシン名', name)
        self.db.set('開始時刻', time.time())
        self.db.set('遷移履歴', [])
        self.db.set('状態データ', {})
    
    def add_state(self, state_name: str, entry_action: Optional[Callable] = None, exit_action: Optional[Callable] = None):
        """状態を追加"""
        self.states[state_name] = {
            'entry_action': entry_action,
            'exit_action': exit_action
        }
    
    def add_transition(self, from_state: str, to_state: str, event: str, guard: Optional[Callable] = None, action: Optional[Callable] = None):
        """遷移を追加"""
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        
        self.transitions[from_state][event] = {
            'to_state': to_state,
            'guard': guard,
            'action': action
        }
    
    def set_initial_state(self, state_name: str):
        """初期状態を設定"""
        if state_name not in self.states:
            raise ValueError(f"未定義の状態: {state_name}")
        
        self.current_state = state_name
        self.db.set('現在の状態', state_name)
        self.db.set('状態開始時刻', time.time())
        
        # エントリーアクション実行
        entry_action = self.states[state_name].get('entry_action')
        if entry_action:
            with self.db.scope(f'エントリー_{state_name}'):
                entry_action(self)
    
    def fire_event(self, event: str, data: Optional[Dict[str, Any]] = None) -> TransitionResult:
        """イベントを発火して状態遷移を試行"""
        if not self.current_state:
            return TransitionResult.ERROR
        
        if self.current_state not in self.transitions:
            return TransitionResult.FORBIDDEN
        
        if event not in self.transitions[self.current_state]:
            return TransitionResult.FORBIDDEN
        
        transition = self.transitions[self.current_state][event]
        to_state = transition['to_state']
        
        # 遷移スコープで処理
        with self.db.scope(f'遷移_{self.current_state}_to_{to_state}'):
            # イベントデータを設定
            if data:
                for key, value in data.items():
                    self.db.set(f'イベント.{key}', value)
            
            self.db.set('イベント名', event)
            self.db.set('元の状態', self.current_state)
            self.db.set('遷移先状態', to_state)
            
            # ガード条件チェック
            guard = transition.get('guard')
            if guard and not guard(self):
                return TransitionResult.FAILED
            
            # 現在の状態のエグジットアクション
            exit_action = self.states[self.current_state].get('exit_action')
            if exit_action:
                exit_action(self)
            
            # 遷移アクション
            action = transition.get('action')
            if action:
                action(self)
            
            # 状態変更
            old_state = self.current_state
            self.current_state = to_state
            self.db.set('現在の状態', to_state)
            self.db.set('状態開始時刻', time.time())
            
            # 遷移履歴を記録
            history = self.db.get('遷移履歴')
            history.append({
                '時刻': time.time(),
                '元の状態': old_state,
                '遷移先状態': to_state,
                'イベント': event,
                'データ': data or {}
            })
            self.db.set('遷移履歴', history)
            
            # 新しい状態のエントリーアクション
            entry_action = self.states[to_state].get('entry_action')
            if entry_action:
                with self.db.scope(f'エントリー_{to_state}'):
                    entry_action(self)
            
            return TransitionResult.SUCCESS
    
    def get_current_state(self) -> str:
        """現在の状態を取得"""
        return self.current_state
    
    def get_state_data(self, key: str, default: Any = None) -> Any:
        """状態データを取得"""
        return self.db.get(f'状態データ.{key}', default)
    
    def set_state_data(self, key: str, value: Any):
        """状態データを設定"""
        self.db.set(f'状態データ.{key}', value)
    
    def get_transition_history(self) -> List[Dict[str, Any]]:
        """遷移履歴を取得"""
        return self.db.get('遷移履歴', [])
    
    def get_available_events(self) -> List[str]:
        """現在の状態で利用可能なイベントを取得"""
        if not self.current_state or self.current_state not in self.transitions:
            return []
        return list(self.transitions[self.current_state].keys())


def door_state_machine_demo():
    """ドアのステートマシンデモ"""
    print("=== ドアのステートマシン ===")
    
    door = StateMachine("自動ドア")
    
    # 状態を定義
    def door_closed_entry(sm):
        print("ドアが閉まりました")
        sm.set_state_data('開放時間', 0)
    
    def door_open_entry(sm):
        print("ドアが開きました")
        sm.set_state_data('開放時間', time.time())
    
    def door_locked_entry(sm):
        print("ドアがロックされました")
        sm.set_state_data('ロック時刻', time.time())
    
    door.add_state("閉", entry_action=door_closed_entry)
    door.add_state("開", entry_action=door_open_entry)
    door.add_state("ロック", entry_action=door_locked_entry)
    
    # 遷移を定義
    def can_open(sm):
        """開くことができるかチェック"""
        return sm.get_state_data('故障中', False) == False
    
    def can_lock(sm):
        """ロックできるかチェック"""
        return sm.get_current_state() == "閉"
    
    def unlock_action(sm):
        """アンロックアクション"""
        unlock_code = sm.db.get('イベント.コード')
        correct_code = sm.get_state_data('ロックコード', '1234')
        if unlock_code != correct_code:
            raise ValueError("間違ったコードです")
        print(f"正しいコード '{unlock_code}' でアンロックしました")
    
    door.add_transition("閉", "開", "人感センサー", guard=can_open)
    door.add_transition("開", "閉", "タイマー")
    door.add_transition("閉", "ロック", "ロック", guard=can_lock)
    door.add_transition("ロック", "閉", "アンロック", action=unlock_action)
    
    # 初期状態設定
    door.set_initial_state("閉")
    door.set_state_data('ロックコード', '1234')
    
    # シナリオ実行
    print(f"現在の状態: {door.get_current_state()}")
    print(f"利用可能なイベント: {door.get_available_events()}")
    
    # ドアを開く
    result = door.fire_event("人感センサー")
    print(f"遷移結果: {result.value}")
    print(f"現在の状態: {door.get_current_state()}")
    
    # ドアを閉める
    result = door.fire_event("タイマー")
    print(f"遷移結果: {result.value}")
    print(f"現在の状態: {door.get_current_state()}")
    
    # ドアをロック
    result = door.fire_event("ロック")
    print(f"遷移結果: {result.value}")
    print(f"現在の状態: {door.get_current_state()}")
    
    # 間違ったコードでアンロック試行
    try:
        result = door.fire_event("アンロック", {"コード": "0000"})
    except ValueError as e:
        print(f"アンロック失敗: {e}")
    
    # 正しいコードでアンロック
    result = door.fire_event("アンロック", {"コード": "1234"})
    print(f"遷移結果: {result.value}")
    print(f"現在の状態: {door.get_current_state()}")
    
    # 遷移履歴表示
    print("\n遷移履歴:")
    for i, transition in enumerate(door.get_transition_history()):
        print(f"  {i+1}. {transition['元の状態']} → {transition['遷移先状態']} (イベント: {transition['イベント']})")
    
    print()


def vending_machine_demo():
    """自動販売機のステートマシンデモ"""
    print("=== 自動販売機のステートマシン ===")
    
    vending = StateMachine("自動販売機")
    
    # 商品情報を初期化
    products = {
        'A1': {'名前': 'コーラ', '価格': 120, '在庫': 5},
        'B1': {'名前': 'オレンジジュース', '価格': 130, '在庫': 3},
        'C1': {'名前': 'コーヒー', '価格': 100, '在庫': 0},  # 在庫切れ
    }
    
    # 状態定義
    def idle_entry(sm):
        print("待機中...")
        sm.set_state_data('投入金額', 0)
        sm.set_state_data('選択商品', None)
    
    def money_inserted_entry(sm):
        amount = sm.get_state_data('投入金額', 0)
        print(f"金額投入状態: {amount}円")
    
    def dispensing_entry(sm):
        product_code = sm.get_state_data('選択商品')
        product = products[product_code]
        print(f"{product['名前']}を提供中...")
        
        # 在庫減少
        products[product_code]['在庫'] -= 1
        
        # お釣り計算
        inserted = sm.get_state_data('投入金額')
        price = product['価格']
        change = inserted - price
        sm.set_state_data('お釣り', change)
    
    def out_of_service_entry(sm):
        print("サービス停止中")
    
    vending.add_state("待機", entry_action=idle_entry)
    vending.add_state("金額投入済み", entry_action=money_inserted_entry)
    vending.add_state("商品提供中", entry_action=dispensing_entry)
    vending.add_state("サービス停止", entry_action=out_of_service_entry)
    
    # ガード関数定義
    def has_sufficient_money(sm):
        """十分な金額が投入されているかチェック"""
        product_code = sm.db.get('イベント.商品コード')
        if product_code not in products:
            return False
        
        inserted = sm.get_state_data('投入金額', 0)
        price = products[product_code]['価格']
        return inserted >= price
    
    def has_stock(sm):
        """在庫があるかチェック"""
        product_code = sm.db.get('イベント.商品コード')
        if product_code not in products:
            return False
        return products[product_code]['在庫'] > 0
    
    def product_available(sm):
        """商品が利用可能かチェック"""
        return has_sufficient_money(sm) and has_stock(sm)
    
    # アクション関数定義
    def add_money_action(sm):
        """金額追加アクション"""
        amount = sm.db.get('イベント.金額', 0)
        current = sm.get_state_data('投入金額', 0)
        new_amount = current + amount
        sm.set_state_data('投入金額', new_amount)
        print(f"{amount}円投入。合計: {new_amount}円")
    
    def select_product_action(sm):
        """商品選択アクション"""
        product_code = sm.db.get('イベント.商品コード')
        sm.set_state_data('選択商品', product_code)
        print(f"商品 {product_code} を選択")
    
    def dispense_complete_action(sm):
        """商品提供完了アクション"""
        change = sm.get_state_data('お釣り', 0)
        if change > 0:
            print(f"お釣り: {change}円")
        print("ありがとうございました")
    
    def return_money_action(sm):
        """返金アクション"""
        amount = sm.get_state_data('投入金額', 0)
        if amount > 0:
            print(f"{amount}円を返金します")
        sm.set_state_data('投入金額', 0)
    
    # 遷移定義
    vending.add_transition("待機", "金額投入済み", "金額投入", action=add_money_action)
    vending.add_transition("金額投入済み", "金額投入済み", "金額投入", action=add_money_action)
    vending.add_transition("金額投入済み", "商品提供中", "商品選択", 
                          guard=product_available, action=select_product_action)
    vending.add_transition("商品提供中", "待機", "提供完了", action=dispense_complete_action)
    vending.add_transition("金額投入済み", "待機", "返金", action=return_money_action)
    vending.add_transition("待機", "サービス停止", "メンテナンス")
    vending.add_transition("サービス停止", "待機", "メンテナンス完了")
    
    # 初期状態設定
    vending.set_initial_state("待機")
    
    # シナリオ実行
    print("商品一覧:")
    for code, product in products.items():
        status = "在庫あり" if product['在庫'] > 0 else "在庫切れ"
        print(f"  {code}: {product['名前']} {product['価格']}円 ({status})")
    
    print(f"\n現在の状態: {vending.get_current_state()}")
    
    # 100円投入
    result = vending.fire_event("金額投入", {"金額": 100})
    print(f"遷移結果: {result.value}")
    
    # コーヒーを選択（在庫切れ）
    result = vending.fire_event("商品選択", {"商品コード": "C1"})
    print(f"遷移結果: {result.value}")  # 失敗するはず
    
    # さらに50円投入
    result = vending.fire_event("金額投入", {"金額": 50})
    print(f"遷移結果: {result.value}")
    
    # オレンジジュースを選択（150円 > 130円なので成功）
    result = vending.fire_event("商品選択", {"商品コード": "B1"})
    print(f"遷移結果: {result.value}")
    
    # 商品提供完了
    result = vending.fire_event("提供完了")
    print(f"遷移結果: {result.value}")
    
    print(f"最終状態: {vending.get_current_state()}")
    
    print()


def workflow_state_machine_demo():
    """ワークフローのステートマシンデモ"""
    print("=== ワークフローのステートマシン ===")
    
    workflow = StateMachine("申請ワークフロー")
    
    # 状態定義
    def draft_entry(sm):
        print("申請書を作成中...")
        sm.set_state_data('作成者', sm.db.get('イベント.作成者', '不明'))
    
    def submitted_entry(sm):
        print("申請書が提出されました")
        sm.set_state_data('提出日時', time.time())
    
    def reviewing_entry(sm):
        reviewer = sm.db.get('イベント.承認者', '不明')
        print(f"{reviewer}さんが審査中...")
        sm.set_state_data('承認者', reviewer)
    
    def approved_entry(sm):
        print("申請が承認されました")
        sm.set_state_data('承認日時', time.time())
    
    def rejected_entry(sm):
        reason = sm.db.get('イベント.理由', '理由不明')
        print(f"申請が却下されました: {reason}")
        sm.set_state_data('却下理由', reason)
    
    workflow.add_state("下書き", entry_action=draft_entry)
    workflow.add_state("提出済み", entry_action=submitted_entry)
    workflow.add_state("審査中", entry_action=reviewing_entry)
    workflow.add_state("承認済み", entry_action=approved_entry)
    workflow.add_state("却下", entry_action=rejected_entry)
    
    # ガード条件
    def can_submit(sm):
        """提出可能かチェック"""
        title = sm.get_state_data('タイトル')
        content = sm.get_state_data('内容')
        return bool(title and content)
    
    def can_approve(sm):
        """承認可能かチェック"""
        reviewer = sm.db.get('イベント.承認者')
        required_reviewer = sm.get_state_data('必要承認者', 'manager')
        return reviewer == required_reviewer
    
    # アクション
    def save_draft_action(sm):
        """下書き保存アクション"""
        title = sm.db.get('イベント.タイトル', '')
        content = sm.db.get('イベント.内容', '')
        sm.set_state_data('タイトル', title)
        sm.set_state_data('内容', content)
        print(f"下書きを保存: {title}")
    
    def submit_action(sm):
        """提出アクション"""
        sm.set_state_data('提出者', sm.db.get('イベント.提出者', '不明'))
        print("申請書を提出しました")
    
    def assign_reviewer_action(sm):
        """承認者割り当てアクション"""
        reviewer = sm.db.get('イベント.承認者')
        print(f"承認者を割り当て: {reviewer}")
    
    # 遷移定義
    workflow.add_transition("下書き", "下書き", "下書き保存", action=save_draft_action)
    workflow.add_transition("下書き", "提出済み", "提出", guard=can_submit, action=submit_action)
    workflow.add_transition("提出済み", "審査中", "承認者割り当て", action=assign_reviewer_action)
    workflow.add_transition("審査中", "承認済み", "承認", guard=can_approve)
    workflow.add_transition("審査中", "却下", "却下")
    workflow.add_transition("却下", "下書き", "再編集")
    
    # 初期状態設定
    workflow.set_initial_state("下書き")
    workflow.set_state_data('必要承認者', 'manager')
    
    # シナリオ実行
    print(f"現在の状態: {workflow.get_current_state()}")
    
    # 下書き作成
    result = workflow.fire_event("下書き保存", {
        "作成者": "田中太郎",
        "タイトル": "新システム導入申請",
        "内容": "新しい販売管理システムの導入を申請します。"
    })
    print(f"遷移結果: {result.value}")
    
    # 提出（内容があるので成功）
    result = workflow.fire_event("提出", {"提出者": "田中太郎"})
    print(f"遷移結果: {result.value}")
    
    # 承認者割り当て
    result = workflow.fire_event("承認者割り当て", {"承認者": "manager"})
    print(f"遷移結果: {result.value}")
    
    # 間違った承認者での承認試行（失敗）
    result = workflow.fire_event("承認", {"承認者": "user"})
    print(f"承認試行結果: {result.value}")
    
    # 正しい承認者での承認
    result = workflow.fire_event("承認", {"承認者": "manager"})
    print(f"承認結果: {result.value}")
    
    print(f"最終状態: {workflow.get_current_state()}")
    
    # ワークフロー情報表示
    print("\nワークフロー情報:")
    print(f"  作成者: {workflow.get_state_data('作成者')}")
    print(f"  タイトル: {workflow.get_state_data('タイトル')}")
    print(f"  承認者: {workflow.get_state_data('承認者')}")
    print(f"  承認日時: {workflow.get_state_data('承認日時')}")
    
    print()


if __name__ == "__main__":
    door_state_machine_demo()
    vending_machine_demo()
    workflow_state_machine_demo()
    
    print("=== まとめ ===")
    print("EphemeralDBを使用することで、ステートマシンの")
    print("状態データと遷移コンテキストを適切に管理できます。")
    print("複雑な業務フローや機器制御にも応用可能です。")