from datetime import datetime
from typing import List, Literal
from src.domain.account.value_objects import AccountId, Amount

class Transaction:
    def __init__(self, transaction_id: str, amount: Amount, transaction_type: Literal['CREDIT', 'DEBIT']):
        self.id = transaction_id
        self.amount = amount
        self.type = transaction_type
        self.created_at = datetime.now()


class Account:
    def __init__(self, account_id: AccountId, initial_balance: float = 0.0):
        self._id = account_id
        self._balance = initial_balance
        self._transactions: List[Transaction] = []
        self._status: Literal['ACTIVE', 'BLOCKED'] = 'ACTIVE'

    @property
    def id(self) -> AccountId:
        return self._id

    @property
    def balance(self) -> float:
        return self._balance

    def debit(self, transaction_id: str, amount: Amount) -> None:
        self._validate_account_state()
        if self._balance < amount.value:
            raise ValueError("Saldo insuficiente para realizar o débito.")

        transaction = Transaction(transaction_id, amount, 'DEBIT')
        self._transactions.append(transaction)
        self._balance -= amount.value

    def credit(self, transaction_id: str, amount: Amount) -> None:
        self._validate_account_state()
        transaction = Transaction(transaction_id, amount, 'CREDIT')
        self._transactions.append(transaction)
        self._balance += amount.value

    def _validate_account_state(self) -> None:
        if self._status != 'ACTIVE':
            raise PermissionError("Operação negada: A conta não está ativa.")

