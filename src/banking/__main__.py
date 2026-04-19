"""Prosty entry point projektu."""

from . import Account, Customer


def main() -> None:
    customer = Customer("Jane", "Simms")
    account = Account(100.0)
    customer.add_account(account)

    account.deposit(50.0)
    account.withdraw(25.0)

    print(customer)
    print(account)


if __name__ == "__main__":
    main()
