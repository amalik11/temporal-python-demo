import random
import string

class InsufficientFundsError(Exception):
    pass

class InvalidAccountError(Exception):
    pass

class account:
    def __init__(self, account_number, balance):
        self.AccountNumber = account_number
        self.Balance = balance

class bank:
    def __init__(self, accounts):
        self.Accounts = accounts

    def findAccount(self, account_number):
        for acc in self.Accounts:
            if acc.AccountNumber == account_number:
                return acc
        return None

mockBank = bank([
    account("85-150", 2000),
    account("43-812", 0)
])

class BankingService:
    def __init__(self, hostname):
        self.Hostname = hostname

    def Withdraw(self, account_number, amount, reference_id):
        acct = mockBank.findAccount(account_number)

        if acct is None:
            raise InvalidAccountError()

        if amount > acct.Balance:
            raise InsufficientFundsError()

        return self.generateTransactionID("W", 10)

    def Deposit(self, account_number, amount, reference_id):
        if mockBank.findAccount(account_number) is None:
            raise InvalidAccountError()

        return self.generateTransactionID("D", 10)

    def DepositThatFails(self, account_number, amount, reference_id):
        raise Exception("This deposit has failed.")

    def generateTransactionID(self, prefix, length):
        allowed_chars = "0123456789"
        rand_chars = [random.choice(allowed_chars) for _ in range(length)]
        return prefix + ''.join(rand_chars)
