from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import uuid

from src.domain.account.account import Account
from src.domain.account.value_objects import AccountId, Amount
from src.infrastructure.repositories.memory_account_repository import MemoryAccountRepository

router = APIRouter()

# Instância única do repositório em memória para a demonstração da API
repository = MemoryAccountRepository()

class CreateAccountRequest(BaseModel):
    initial_balance: float = 0.0

class TransactionRequest(BaseModel):
    amount: float

@router.post("/accounts", status_code=201)
def create_account(request: CreateAccountRequest):
    account_id_str = f"acc-{uuid.uuid4().hex[:8]}"
    account = Account(AccountId(account_id_str), request.initial_balance)
    repository.save(account)
    return {"account_id": account.id.value, "balance": account.balance}

@router.post("/accounts/{account_id}/credit")
def credit_account(account_id: str, request: TransactionRequest):
    account = repository.find_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        tx_id = f"tx-{uuid.uuid4().hex[:8]}"
        account.credit(tx_id, Amount(request.amount))
        repository.save(account)
        return {"message": "Crédito realizado", "new_balance": account.balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/accounts/{account_id}/debit")
def debit_account(account_id: str, request: TransactionRequest):
    account = repository.find_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        tx_id = f"tx-{uuid.uuid4().hex[:8]}"
        account.debit(tx_id, Amount(request.amount))
        repository.save(account)
        return {"message": "Débito realizado", "new_balance": account.balance}
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))

