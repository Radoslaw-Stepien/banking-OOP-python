"""Podstawowy model domenowy projektu bankowego."""


class Account:
    """Klasa reprezentujaca konto bankowe."""

    def __init__(self, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Saldo poczatkowe nie moze byc ujemne")
        self.__balance = balance

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            return False
        if amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def get_balance(self) -> float:
        return self.__balance

    def __str__(self) -> str:
        return f"Wartosc konta = {self.__balance}"


class Customer:
    """Klasa reprezentujaca klienta banku."""

    def __init__(self, first_name: str, last_name: str):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__accounts: list[Account] = []

    def add_account(self, account: Account) -> None:
        self.__accounts.append(account)

    def get_account(self, index: int) -> Account | None:
        if index < 0 or index >= len(self.__accounts):
            return None
        return self.__accounts[index]

    def get_number_of_accounts(self) -> int:
        return len(self.__accounts)

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def __str__(self) -> str:
        return (
            f"Customer{{firstName='{self.__first_name}', "
            f"lastName='{self.__last_name}', "
            f"number_of_accounts={self.get_number_of_accounts()}}}"
        )
