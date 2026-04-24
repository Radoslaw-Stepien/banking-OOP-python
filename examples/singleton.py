class BankConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.interest_rate = 0.05
        return cls._instance

if __name__ == "__main__":
    config1 = BankConfig()
    config2 = BankConfig()

    print("Ten sam obiekt?", config1 is config2)
    print("Stopa procentowa:", config1.interest_rate)

    config1.interest_rate = 0.07
    print("Po zmianie przez config1:", config2.interest_rate)
