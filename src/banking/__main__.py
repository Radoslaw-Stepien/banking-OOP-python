"""Prosty entry point projektu."""

from . import Customer, SavingsAccount, CheckingAccount

def main() -> None:
    customer = Customer("Jane", "Simms")
    savings_account = SavingsAccount(100.0)
    checking_account = CheckingAccount(200.0, 50.0)

    customer.add_account(savings_account)
    customer.add_account(checking_account)

    savings_account.deposit(25.0)
    checking_account.withdraw(220.0)

    print(customer)
    print(savings_account)
    print(checking_account)

if __name__ == "__main__":
    main()

