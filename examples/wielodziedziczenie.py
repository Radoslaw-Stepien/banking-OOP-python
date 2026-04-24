class Loggable:
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")

class Notifiable:
    def notify(self, message: str) -> None:
        print(f"[NOTIFY] {message}")

class PremiumAccount(Loggable, Notifiable):
    def __init__(self, balance: float = 0.0):
        self.__balance = balance

    def deposit(self, amount: float) -> None:
        self.__balance += amount
        self.log(f"Wplata: {amount}")
        self.notify(f"Saldo po wplacie: {self.__balance}")

    def get_balance(self) -> float:
        return self.__balance

if __name__ == "__main__":
    konto = PremiumAccount(100.0)
    konto.deposit(50.0)
    print("Saldo:", konto.get_balance())

