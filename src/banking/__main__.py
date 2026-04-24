"""Prosty entry point projektu."""

from . import Customer, SavingsAccount, CheckingAccount, Bank

def main() -> None:
    bank = Bank()

    jan = Customer("Jan", "Kowalski")
    jan.add_account(SavingsAccount(1000.0))
    jan.add_account(CheckingAccount(500.0, 200.0))

    anna = Customer("Anna", "Nowak")
    anna.add_account(SavingsAccount(2000.0))

    bank.add_customer(jan)
    bank.add_customer(anna)

    jan.get_account(0).deposit(500.0)
    bank.transfer(jan.get_account(1), anna.get_account(0), 300.0)

    jan.get_account(0).apply_monthly_update()
    jan.get_account(1).apply_monthly_update()
    anna.get_account(0).apply_monthly_update()

    print(f"Liczba klientow: {bank.get_number_of_customers()}")
    print(f"Laczne saldo banku: {bank.get_total_balance():.2f}")
    print()

    report = bank.generate_report()
    for name, balance in report.items():
          print(f" {name}: {balance:.2f}")

if __name__ == "__main__":
    main()
