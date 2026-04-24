from typing import Protocol

class Summarizable(Protocol):
    def summary(self) -> str:
        ...

class AccountSummary:
    def __init__(self, owner: str, balance: float):
        self.__owner = owner
        self.__balance = balance

    def summary(self) -> str:
        return f"{self.__owner}: {self.__balance} PLN"

def print_summary(item: Summarizable) -> None:
    print(item.summary())

if __name__ == "__main__":
    acc = AccountSummary("Jan Kowalski", 1500.0)
    print_summary(acc)
