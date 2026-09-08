class AccountId:
    def __init__(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("AccountId inválido.")
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Amount:
    def __init__(self, value: float, currency: str = "BRL"):
        if value <= 0:
            raise ValueError("O valor da operação deve ser maior que zero.")
        self._value = value
        self._currency = currency

    @property
    def value(self) -> float:
        return self._value

    @property
    def currency(self) -> str:
        return self._currency

