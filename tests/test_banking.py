import unittest

from banking import Account, Customer, SavingsAccount, CheckingAccount, Bank, TransactionType


class AccountTests(unittest.TestCase):
    def test_deposit_increases_balance(self) -> None:
        account = SavingsAccount(100.0)

        result = account.deposit(50.0)

        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 150.0)

    def test_deposit_rejects_non_positive_amount(self) -> None:
        account = SavingsAccount(100.0)

        result = account.deposit(0)

        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 100.0)

    def test_withdraw_rejects_amount_above_balance(self) -> None:
        account = SavingsAccount(100.0)

        result = account.withdraw(150.0)

        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 100.0)

class SavingsAccountTests(unittest.TestCase):
    def test_savings_account_keeps_initial_balance(self) -> None:
        account = SavingsAccount(200.0)

        self.assertEqual(account.get_balance(), 200.0)

    def test_savings_account_rejects_negative_initial_balance(self) -> None:
        with self.assertRaises(ValueError):
            SavingsAccount(-10.0)

class CheckingAccountTests(unittest.TestCase):
    def test_checking_account_stores_overdraft_limit(self) -> None:
        account = CheckingAccount(100.0, 50.0)

        self.assertEqual(account.get_balance(), 100.0)
        self.assertEqual(account.get_overdraft_limit(), 50.0)

    def test_checking_account_allow_withdraw_within_overdraft_limit(self) -> None:
        account = CheckingAccount(100.0, 50.0)

        result = account.withdraw(120.0)

        self.assertTrue(result)
        self.assertEqual(account.get_balance(), -20.0)

    def test_checking_account_rejects_withdraw_above_overdraft_limit(self) -> None:
        account = CheckingAccount(100.0, 50.0)

        result = account.withdraw(160.0)

        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 100.0)

    def test_checking_account_rejects_negative_overdraft_limit(self) -> None:
        with self.assertRaises(ValueError):
            CheckingAccount(100.0, -10.0)

    def test_checking_account_rejects_zero_withdraw(self) -> None:
        account = CheckingAccount(100.0, 50.0)

        result = account.withdraw(0)
        
        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 100.0)

    def test_checking_account_rejects_negative_withdraw(self) -> None:
        account = CheckingAccount(100.0, 50.0)

        result = account.withdraw(-10.0)

        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 100.0)

class CustomerTests(unittest.TestCase):
    def test_customer_can_store_multiple_accounts(self) -> None:
        customer = Customer("Jane", "Simms")
        first = SavingsAccount(100.0)
        second = SavingsAccount(250.0)

        customer.add_account(first)
        customer.add_account(second)

        self.assertEqual(customer.get_number_of_accounts(), 2)
        self.assertIs(customer.get_account(0), first)
        self.assertIs(customer.get_account(1), second)

class BankTests(unittest.TestCase):
    def test_bank_counts_customers(self) -> None:
        bank = Bank()
        customer = Customer("Jan", "Kowalski")

        bank.add_customer(customer)

        self.assertEqual(bank.get_number_of_customers(), 1)

    def test_bank_returns_customer_by_index(self) -> None:
        bank = Bank()
        customer = Customer("Jan", "Kowalski")

        bank.add_customer(customer)

        self.assertIs(bank.get_customer(0), customer)
        self.assertIsNone(bank.get_customer(1))

    def test_transfer_moves_funds_between_accounts(self) -> None:
        bank = Bank()
        source = SavingsAccount(100.0)
        target = SavingsAccount(50.0)

        result = bank.transfer(source, target, 30.0)

        self.assertTrue(result)
        self.assertEqual(source.get_balance(), 70.0)
        self.assertEqual(target.get_balance(), 80.0)

    def test_transfer_fails_when_source_has_insufficient_funds(self) -> None:
        bank = Bank()
        source = SavingsAccount(20.0)
        target = SavingsAccount(50.0)

        result = bank.transfer(source, target, 100.0)

        self.assertFalse(result)
        self.assertEqual(source.get_balance(), 20.0)
        self.assertEqual(target.get_balance(), 50.0)
class TransactionTests(unittest.TestCase):
    
    def test_deposit_creates_transaction(self):
        account = SavingsAccount(100.0)
        account.deposit(50.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].get_type(), TransactionType.DEPOSIT)
        self.assertEqual(transactions[0].get_amount(), 50.0)

    def test_withdrawal_create_transactions(self):
        account = SavingsAccount(100.0)
        account.withdraw(30.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].get_type(), TransactionType.WITHDRAWAL)
        self.assertEqual(transactions[0].get_amount(), 30.0)

class MonthUpdateTests(unittest.TestCase):

    def test_savings_account_applies_interest(self):
        account = SavingsAccount(1200.0)
        account.apply_monthly_update()
        self.assertAlmostEqual(account.get_balance(), 1205.0, places=2)

    def test_checking_account_applies_fee(self):
        account = CheckingAccount(100.0)
        account.apply_monthly_update()
        self.assertEqual(account.get_balance(), 95.0)

class StaticMethodTests(unittest.TestCase):

    def test_is_valid_amount_accepts_positives(self):
        self.assertTrue(Account.is_valid_amount(10.0))

    def test_is_valid_amount_rejects_zero(self):
        self.assertFalse(Account.is_valid_amount(0))

    def test_is_valid_amount_rejects_negative(self):
        self.assertFalse(Account.is_valid_amount(-5.0))

if __name__ == "__main__":
    unittest.main()
