import os
import unittest

from banking import (
    Account, Customer, SavingsAccount, CheckingAccount, Bank, TransactionType
)


class AccountTests(unittest.TestCase):
    def test_deposit_increases_balance(self) -> None:
        """Wplata dodatnia zwieksza saldo."""
        account = SavingsAccount(100.0)
        account.deposit(50.0)
        self.assertEqual(account.get_balance(), 150.0)

    def test_deposit_rejects_non_positive_amount(self) -> None:
        """Wplata zerowa lub ujemna rzuca ValueError — saldo bez zmian."""
        account = SavingsAccount(100.0)
        with self.assertRaises(ValueError):
            account.deposit(0)
        self.assertEqual(account.get_balance(), 100.0)

    def test_withdraw_rejects_amount_above_balance(self) -> None:
        """Wyplata powyzej salda rzuca ValueError — saldo bez zmian."""
        account = SavingsAccount(100.0)
        with self.assertRaises(ValueError):
            account.withdraw(150.0)
        self.assertEqual(account.get_balance(), 100.0)


class SavingsAccountTests(unittest.TestCase):
    def test_savings_account_keeps_initial_balance(self) -> None:
        """Saldo poczatkowe jest zachowane po utworzeniu konta."""
        account = SavingsAccount(200.0)
        self.assertEqual(account.get_balance(), 200.0)

    def test_savings_account_rejects_negative_initial_balance(self) -> None:
        """Ujemne saldo poczatkowe rzuca ValueError."""
        with self.assertRaises(ValueError):
            SavingsAccount(-10.0)


class CheckingAccountTests(unittest.TestCase):
    def test_checking_account_stores_overdraft_limit(self) -> None:
        """Konto biezace przechowuje saldo i limit debetowy."""
        account = CheckingAccount(100.0, 50.0)
        self.assertEqual(account.get_balance(), 100.0)
        self.assertEqual(account.get_overdraft_limit(), 50.0)

    def test_checking_account_allow_withdraw_within_overdraft_limit(
            self) -> None:
        """Wyplata w granicach salda + limitu jest dozwolona."""
        account = CheckingAccount(100.0, 50.0)
        account.withdraw(120.0)
        self.assertEqual(account.get_balance(), -20.0)

    def test_checking_account_rejects_withdraw_above_overdraft_limit(
            self) -> None:
        """Wyplata powyzej salda + limitu rzuca ValueError."""
        account = CheckingAccount(100.0, 50.0)
        with self.assertRaises(ValueError):
            account.withdraw(160.0)
        self.assertEqual(account.get_balance(), 100.0)

    def test_checking_account_rejects_negative_overdraft_limit(self) -> None:
        """Ujemny limit debetowy rzuca ValueError."""
        with self.assertRaises(ValueError):
            CheckingAccount(100.0, -10.0)

    def test_checking_account_rejects_zero_withdraw(self) -> None:
        """Wyplata zerowa rzuca ValueError."""
        account = CheckingAccount(100.0, 50.0)
        with self.assertRaises(ValueError):
            account.withdraw(0)
        self.assertEqual(account.get_balance(), 100.0)

    def test_checking_account_rejects_negative_withdraw(self) -> None:
        """Wyplata ujemna rzuca ValueError."""
        account = CheckingAccount(100.0, 50.0)
        with self.assertRaises(ValueError):
            account.withdraw(-10.0)
        self.assertEqual(account.get_balance(), 100.0)

    def test_checking_account_records_withdrawal_transaction(self) -> None:
        """Wyplata z konta biezacego jest zapisywana w historii transakcji."""
        account = CheckingAccount(100.0, 50.0)
        account.withdraw(40.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(
            transactions[0].get_type(),
            TransactionType.WITHDRAWAL)
        self.assertEqual(transactions[0].get_amount(), 40.0)


class CustomerTests(unittest.TestCase):
    def test_customer_can_store_multiple_accounts(self) -> None:
        """Klient przechowuje wiele kont i zwraca je po indeksie."""
        customer = Customer("Jane", "Simms")
        first = SavingsAccount(100.0)
        second = SavingsAccount(250.0)

        customer.add_account(first)
        customer.add_account(second)

        self.assertEqual(customer.get_number_of_accounts(), 2)
        self.assertIs(customer.get_account(0), first)
        self.assertIs(customer.get_account(1), second)

    def test_get_accounts_returns_all_accounts(self) -> None:
        """get_accounts zwraca liste wszystkich kont klienta."""
        customer = Customer("Jane", "Simms")
        first = SavingsAccount(100.0)
        second = CheckingAccount(200.0, 50.0)

        customer.add_account(first)
        customer.add_account(second)

        accounts = customer.get_accounts()
        self.assertEqual(len(accounts), 2)
        self.assertIn(first, accounts)
        self.assertIn(second, accounts)

    def test_customer_get_account_out_of_range_raises_error(self) -> None:
        """get_account z indeksem poza zakresem rzuca IndexError."""
        customer = Customer("Jane", "Simms")
        customer.add_account(SavingsAccount(100.0))
        with self.assertRaises(IndexError):
            customer.get_account(1)

    def test_customer_rejects_empty_name(self) -> None:
        """Pusty ciag jako imie lub nazwisko rzuca ValueError."""
        with self.assertRaises(ValueError):
            Customer("", "Kowalski")
        with self.assertRaises(ValueError):
            Customer("Jan", "")


class BankTests(unittest.TestCase):
    def test_bank_counts_customers(self) -> None:
        """Bank poprawnie zlicza dodanych klientow."""
        bank = Bank()
        bank.add_customer(Customer("Jan", "Kowalski"))
        self.assertEqual(bank.get_number_of_customers(), 1)

    def test_bank_returns_customer_by_index(self) -> None:
        """Bank zwraca klienta po indeksie."""
        bank = Bank()
        customer = Customer("Jan", "Kowalski")
        bank.add_customer(customer)
        self.assertIs(bank.get_customer(0), customer)

    def test_bank_get_customer_out_of_range_raises_error(self) -> None:
        """get_customer z indeksem poza zakresem rzuca IndexError."""
        bank = Bank()
        bank.add_customer(Customer("Jan", "Kowalski"))
        with self.assertRaises(IndexError):
            bank.get_customer(1)

    def test_get_customers_returns_all(self) -> None:
        """get_customers zwraca liste wszystkich klientow."""
        bank = Bank()
        jan = Customer("Jan", "Kowalski")
        anna = Customer("Anna", "Nowak")
        bank.add_customer(jan)
        bank.add_customer(anna)
        customers = bank.get_customers()
        self.assertEqual(len(customers), 2)
        self.assertIn(jan, customers)
        self.assertIn(anna, customers)

    def test_transfer_moves_funds_between_accounts(self) -> None:
        """Przelew przenosi srodki: zrodlo traci, cel zyskuje."""
        bank = Bank()
        source = SavingsAccount(100.0)
        target = SavingsAccount(50.0)
        bank.transfer(source, target, 30.0)
        self.assertEqual(source.get_balance(), 70.0)
        self.assertEqual(target.get_balance(), 80.0)

    def test_transfer_fails_when_source_has_insufficient_funds(self) -> None:
        """Przelew rzuca ValueError gdy brak wystarczajacych srodkow."""
        bank = Bank()
        source = SavingsAccount(20.0)
        target = SavingsAccount(50.0)
        with self.assertRaises(ValueError):
            bank.transfer(source, target, 100.0)
        self.assertEqual(source.get_balance(), 20.0)
        self.assertEqual(target.get_balance(), 50.0)

    def test_get_total_balance_sums_all_accounts(self):
        """Laczne saldo banku sumuje wszystkie konta wszystkich klientow."""
        bank = Bank()
        customer = Customer("Jan", "Kowalski")
        customer.add_account(SavingsAccount(100.0))
        customer.add_account(CheckingAccount(50.0))
        bank.add_customer(customer)
        self.assertEqual(bank.get_total_balance(), 150.0)

    def test_generate_report_returns_balance_per_customer(self):
        """Raport zawiera laczne saldo per klient jako slownik."""
        bank = Bank()
        customer = Customer("Jan", "Kowalski")
        customer.add_account(SavingsAccount(200.0))
        bank.add_customer(customer)
        report = bank.generate_report()
        self.assertIn("Jan Kowalski", report)
        self.assertEqual(report["Jan Kowalski"], 200.0)


class TransactionTests(unittest.TestCase):
    def test_deposit_creates_transaction(self):
        """Wplata tworzy rekord transakcji typu DEPOSIT z prawidlowa kwota."""
        account = SavingsAccount(100.0)
        account.deposit(50.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].get_type(), TransactionType.DEPOSIT)
        self.assertEqual(transactions[0].get_amount(), 50.0)

    def test_withdrawal_creates_transaction(self):
        """Wyplata tworzy rekord transakcji WITHDRAWAL z prawidlowa kwota."""
        account = SavingsAccount(100.0)
        account.withdraw(30.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(
            transactions[0].get_type(),
            TransactionType.WITHDRAWAL)
        self.assertEqual(transactions[0].get_amount(), 30.0)


class MonthUpdateTests(unittest.TestCase):
    def test_savings_account_applies_interest(self):
        """Konto oszczednosciowe nalicza miesieczne odsetki (5% rocznie)."""
        account = SavingsAccount(1200.0)
        account.apply_monthly_update()
        self.assertAlmostEqual(account.get_balance(), 1205.0, places=2)

    def test_checking_account_applies_fee(self):
        """Konto biezace pobiera miesieczna oplate 5 zl."""
        account = CheckingAccount(100.0)
        account.apply_monthly_update()
        self.assertEqual(account.get_balance(), 95.0)


class StaticMethodTests(unittest.TestCase):
    def test_is_valid_amount_accepts_positives(self):
        """Kwota dodatnia jest uznawana za poprawna."""
        self.assertTrue(Account.is_valid_amount(10.0))

    def test_is_valid_amount_rejects_zero(self):
        """Zero jest niepoprawna kwota operacji."""
        self.assertFalse(Account.is_valid_amount(0))

    def test_is_valid_amount_rejects_negative(self):
        """Kwota ujemna jest niepoprawna."""
        self.assertFalse(Account.is_valid_amount(-5.0))


class FileIOTests(unittest.TestCase):
    FILEPATH = "test_bank_state_tmp.json"

    def setUp(self):
        self.bank = Bank()
        customer = Customer("Jan", "Kowalski")
        customer.add_account(SavingsAccount(1000.0))
        customer.add_account(CheckingAccount(500.0, 200.0))
        self.bank.add_customer(customer)

    def tearDown(self):
        if os.path.exists(self.FILEPATH):
            os.remove(self.FILEPATH)

    def test_save_and_load_restores_customers(self):
        """Zapis i odczyt przywracaja liste klientow i ich dane."""
        self.bank.save_to_file(self.FILEPATH)
        new_bank = Bank()
        new_bank.load_from_file(self.FILEPATH)
        self.assertEqual(new_bank.get_number_of_customers(), 1)
        customer = new_bank.get_customer(0)
        self.assertEqual(customer.get_first_name(), "Jan")
        self.assertEqual(customer.get_last_name(), "Kowalski")

    def test_save_and_load_restores_accounts(self):
        """Zapis i odczyt przywracaja konta z poprawnymi typami i saldami."""
        self.bank.save_to_file(self.FILEPATH)
        new_bank = Bank()
        new_bank.load_from_file(self.FILEPATH)
        customer = new_bank.get_customer(0)
        self.assertEqual(customer.get_number_of_accounts(), 2)
        self.assertIsInstance(customer.get_account(0), SavingsAccount)
        self.assertEqual(customer.get_account(0).get_balance(), 1000.0)
        self.assertIsInstance(customer.get_account(1), CheckingAccount)
        self.assertEqual(customer.get_account(1).get_balance(), 500.0)
        self.assertEqual(customer.get_account(1).get_overdraft_limit(), 200.0)

    def test_load_from_nonexistent_file_raises_error(self):
        """Odczyt nieistniejacego pliku rzuca FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            self.bank.load_from_file("plik_ktory_nie_istnieje.json")

    def test_load_from_invalid_json_raises_value_error(self):
        """Odczyt pliku z niepoprawnym JSON rzuca ValueError."""
        with open(self.FILEPATH, "w") as f:
            f.write("to nie jest json {{{")
        with self.assertRaises(ValueError):
            self.bank.load_from_file(self.FILEPATH)

    def test_load_from_missing_field_raises_value_error(self):
        """Odczyt pliku z brakujacym polem rzuca ValueError."""
        with open(self.FILEPATH, "w") as f:
            f.write('{"customers": [{"first_name": "Jan"}]}')
        with self.assertRaises(ValueError):
            self.bank.load_from_file(self.FILEPATH)

    def test_save_and_load_restores_transaction_history(self):
        """Zapis i odczyt przywracaja pelna historie transakcji."""
        customer = self.bank.get_customer(0)
        account = customer.get_account(0)
        account.deposit(200.0)
        account.withdraw(50.0)

        self.bank.save_to_file(self.FILEPATH)
        new_bank = Bank()
        new_bank.load_from_file(self.FILEPATH)

        restored = new_bank.get_customer(0).get_account(0)
        transactions = restored.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].get_type(), TransactionType.DEPOSIT)
        self.assertEqual(transactions[0].get_amount(), 200.0)
        self.assertEqual(
            transactions[1].get_type(), TransactionType.WITHDRAWAL
        )
        self.assertEqual(transactions[1].get_amount(), 50.0)


if __name__ == "__main__":
    unittest.main()
