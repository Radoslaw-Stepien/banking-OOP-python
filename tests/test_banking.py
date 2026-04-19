import unittest

from banking import Account, Customer


class AccountTests(unittest.TestCase):
    def test_deposit_increases_balance(self) -> None:
        account = Account(100.0)

        result = account.deposit(50.0)

        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 150.0)

    def test_deposit_rejects_non_positive_amount(self) -> None:
        account = Account(100.0)

        result = account.deposit(0)

        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 100.0)

    def test_withdraw_rejects_amount_above_balance(self) -> None:
        account = Account(100.0)

        result = account.withdraw(150.0)

        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 100.0)


class CustomerTests(unittest.TestCase):
    def test_customer_can_store_multiple_accounts(self) -> None:
        customer = Customer("Jane", "Simms")
        first = Account(100.0)
        second = Account(250.0)

        customer.add_account(first)
        customer.add_account(second)

        self.assertEqual(customer.get_number_of_accounts(), 2)
        self.assertIs(customer.get_account(0), first)
        self.assertIs(customer.get_account(1), second)


if __name__ == "__main__":
    unittest.main()
