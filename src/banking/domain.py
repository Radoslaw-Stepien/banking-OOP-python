"""Podstawowy model domenowy projektu bankowego."""

from abc import ABC, abstractmethod
from enum import Enum

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class Transaction:
    def __init__(self, transaction_type: TransactionType, amount: float):
        self.__type = transaction_type
        self.__amount = amount

    def get_type(self) -> TransactionType:
        return self.__type

    def get_amount(self) -> float:
        return self.__amount

class Account(ABC):
    """Klasa reprezentujaca konto bankowe."""

    def __init__(self, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Saldo poczatkowe nie moze byc ujemne")
        self.__balance = balance
        self.__transactions: list[Transaction] = []

    @staticmethod
    def is_valid_amount(amount: float) -> bool:
        return amount > 0

    def deposit(self, amount: float) -> bool:
        if not Account.is_valid_amount(amount):
            return False
            
        self.__balance += amount
        self.__transactions.append(Transaction(TransactionType.DEPOSIT, amount))
        return True

    def withdraw(self, amount: float) -> bool:
        if not Account.is_valid_amount(amount):
            return False

        if amount > self.__balance:
            return False
        self.__balance -= amount
        self.__transactions.append(Transaction(TransactionType.WITHDRAWAL, amount))
        return True

    def get_balance(self) -> float:
        return self.__balance

    def get_transactions(self) -> list[Transaction]:
        return list(self.__transactions)

    def _change_balance(self, amount: float) -> None:
        self.__balance += amount

    def __str__(self) -> str:
        return f"Wartosc konta = {self.__balance}"

    @abstractmethod
    def apply_monthly_update(self) -> None:
        pass

class SavingsAccount(Account):
    """Konto oszczednosciowe."""

    def __init__(self, balance: float = 0.0):
        super().__init__(balance)

    def apply_monthly_update(self) -> None:
        self._change_balance(self.get_balance() * 0.05 / 12)

class CheckingAccount(Account):
    """Konto biezace."""
    def __init__(self, balance: float = 0.0, overdraft_limit: float = 0.0):

        if overdraft_limit < 0:
            raise ValueError("Limit debetowy nie moze byc ujemny")
        super().__init__(balance)
        self.__overdraft_limit = overdraft_limit

    def get_overdraft_limit(self) -> float:
        return self.__overdraft_limit

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            return False
        if amount > self.get_balance() + self.__overdraft_limit:
            return False
        self._change_balance(-amount)
        return True

    def apply_monthly_update(self) -> None:
        self._change_balance(-5.0)

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

class Bank:
    """Klasa reprezentujaca bank."""

    def __init__(self):
        self.__customers = []

    def add_customer(self, customer: Customer) -> None:
        self.__customers.append(customer)

    def get_number_of_customers(self) -> int:
        return len(self.__customers)

    def get_customer(self, index: int) -> Customer | None:
        if index < 0 or index >= len(self.__customers):
            return None
        return self.__customers[index]

    def transfer(self, source: Account, target: Account, amount: float) -> bool:
        if not source.withdraw(amount):
            return False
        target.deposit(amount)
        return True
    
    def get_total_balance(self) -> float:
        total = 0.0
        for customer in self.__customers:
            for i in range(customer.get_number_of_accounts()):
                total += customer.get_account(i).get_balance()
        return total

    def generate_report(self) -> dict[str, float]:
        report = {}
        for customer in self.__customers:
            name = f"{customer.get_first_name()} {customer.get_last_name()}"
            total = 0.0
            for i in range(customer.get_number_of_accounts()):
                total += customer.get_account(i).get_balance()
            report[name] = total
        return report
