"""Podstawowy model domenowy projektu bankowego."""

from abc import ABC, abstractmethod
from enum import Enum
import json

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

    def deposit(self, amount: float) -> None:
        if not Account.is_valid_amount(amount):
            raise ValueError("Kwota wplaty musi byc wieksza od zera")
        self.__balance += amount
        self.__transactions.append(Transaction(TransactionType.DEPOSIT, amount))

    def withdraw(self, amount: float) -> None:
        if not Account.is_valid_amount(amount):
            raise ValueError("Kwota wyplaty musi byc wieksza od zera")
        if amount > self.__balance:
            raise ValueError("Niewystarczajace saldo na koncie")
        self.__balance -= amount
        self.__transactions.append(Transaction(TransactionType.WITHDRAWAL, amount))

    def get_balance(self) -> float:
        return self.__balance

    def get_transactions(self) -> list[Transaction]:
        return list(self.__transactions)

    def _change_balance(self, amount: float) -> None:
        self.__balance += amount

    def _record_transaction(self, transaction_type: TransactionType, amount: float) -> None:
        self.__transactions.append(Transaction(transaction_type, amount))

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

    def to_dict(self) -> dict:
        return {"type": "savings", "balance": self.get_balance()}

class CheckingAccount(Account):
    """Konto biezace."""
    def __init__(self, balance: float = 0.0, overdraft_limit: float = 0.0):

        if overdraft_limit < 0:
            raise ValueError("Limit debetowy nie moze byc ujemny")
        super().__init__(balance)
        self.__overdraft_limit = overdraft_limit

    def get_overdraft_limit(self) -> float:
        return self.__overdraft_limit

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Kwota wyplaty musi byc wieksza od zera")
        if amount > self.get_balance() + self.__overdraft_limit:
            raise ValueError("Przekroczono dostepne saldo i limit debetowy")
        self._change_balance(-amount)
        self._record_transaction(TransactionType.WITHDRAWAL, amount)

    def apply_monthly_update(self) -> None:
        self._change_balance(-5.0)

    def to_dict(self) -> dict:
        return {"type": "checking", "balance": self.get_balance(), "overdraft_limit": self.__overdraft_limit}

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

    def get_accounts(self) -> list[Account]:
        return list(self.__accounts)

    def get_number_of_accounts(self) -> int:
        return len(self.__accounts)

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def to_dict(self) -> dict:
        return {
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "accounts": [self.__accounts[i].to_dict() for i in range(len(self.__accounts))]
        }

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

    def get_customers(self) -> list[Customer]:
        return list(self.__customers)

    def get_number_of_customers(self) -> int:
        return len(self.__customers)

    def get_customer(self, index: int) -> Customer | None:
        if index < 0 or index >= len(self.__customers):
            return None
        return self.__customers[index]

    def transfer(self, source: Account, target: Account, amount: float) -> None:
        source.withdraw(amount)
        target.deposit(amount)
    
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

    def save_to_file(self, filepath: str) -> None:
        try:
            data = {"customers": [c.to_dict() for c in self.__customers]}
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Nie mozna zapisac pliku '{filepath}': {e}") from e

    def load_from_file(self, filepath: str) -> None:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Plik '{filepath}' nie istnieje.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Plik '{filepath}' zawiera nieprawidlowy JSON: {e}") from e
        except IOError as e:
            raise IOError(f"Nie mozna odczytac pliku '{filepath}': {e}") from e

        try:
            self.__customers = []
            for customer_data in data["customers"]:
                customer = Customer(customer_data["first_name"], customer_data["last_name"])
                for account_data in customer_data["accounts"]:
                    if account_data["type"] == "savings":
                        account = SavingsAccount(account_data["balance"])
                    elif account_data["type"] == "checking":
                        account = CheckingAccount(account_data["balance"], account_data["overdraft_limit"])
                    else:
                        raise ValueError(f"Nieznany typ konta: {account_data['type']}")
                    customer.add_account(account)
                self.__customers.append(customer)
        except KeyError as e:
            raise ValueError(f"Nieprawidlowa struktura pliku — brakuje pola: {e}") from e
