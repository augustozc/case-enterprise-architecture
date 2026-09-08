from typing import Dict, Optional
from src.domain.account.account import Account

class MemoryAccountRepository:
    """Implementação do padrão Repository armazenando dados em memória"""
    def __init__(self):
        self._db: Dict[str, Account] = {}

    def save(self, account: Account) -> None:
        self._db[account.id.value] = account

    def find_by_id(self, account_id: str) -> Optional[Account]:
        return self._db.get(account_id)

