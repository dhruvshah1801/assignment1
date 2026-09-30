class InsufficientBalanceError(Exception):
    """Raised when an account does not have enough balance."""
    pass


class AccountNotFoundError(Exception):
    """Raised when an account does not exist."""
    pass


class InvalidAmountError(Exception):
    """Raised when amount is invalid."""
    pass


class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        if amount > self._balance:
            raise InsufficientBalanceError(
                f"Insufficient balance in {self.account_id}"
            )

        self._balance -= amount


class Transaction:
    def __init__(self, operation, details):
        self.operation = operation
        self.details = details


class Bank:
    def __init__(self):
        self.accounts = {}
        self.history = []

    def add_account(self, account_id, balance):
        self.accounts[account_id] = Account(account_id, balance)

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(
                f"Account {account_id} not found"
            )

        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)

        account.deposit(amount)

        self.history.append(
            Transaction("DEPOSIT", (account_id, amount))
        )

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)

        account.withdraw(amount)

        self.history.append(
            Transaction("WITHDRAW", (account_id, amount))
        )

    def transfer(self, from_id, to_id, amount):
        sender = self.get_account(from_id)
        receiver = self.get_account(to_id)

        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        # Check before modifying either account
        if amount > sender.balance:
            raise InsufficientBalanceError(
                f"Insufficient balance in {from_id}"
            )

        sender.withdraw(amount)
        receiver.deposit(amount)

        self.history.append(
            Transaction(
                "TRANSFER",
                (from_id, to_id, amount)
            )
        )


def main():
    bank = Bank()

    # Number of accounts
    n = int(input())

    # Initial accounts
    for _ in range(n):
        account_id, balance = input().split()

        bank.add_account(
            account_id,
            int(balance)
        )

    # Number of operations
    q = int(input())

    failed_batches = 0
    batch_active = False

    # Stores balances before the current batch
    batch_backup = None

    for _ in range(q):
        line = input().strip()

        if not line:
            continue

        parts = line.split()
        operation = parts[0]

        try:

            if operation == "BATCH_BEGIN":

                if batch_active:
                    raise ValueError("Nested batch not allowed")

                batch_active = True

                # Save current balances
                batch_backup = {
                    account_id: account.balance
                    for account_id, account in bank.accounts.items()
                }

            elif operation == "BATCH_END":

                if not batch_active:
                    raise ValueError("BATCH_END without BATCH_BEGIN")

                batch_active = False
                batch_backup = None

            elif operation == "DEPOSIT":

                account_id = parts[1]
                amount = int(parts[2])

                bank.deposit(account_id, amount)

            elif operation == "WITHDRAW":

                account_id = parts[1]
                amount = int(parts[2])

                bank.withdraw(account_id, amount)

            elif operation == "TRANSFER":

                from_id = parts[1]
                to_id = parts[2]
                amount = int(parts[3])

                bank.transfer(
                    from_id,
                    to_id,
                    amount
                )

            else:
                raise ValueError("Unknown operation")

        except Exception:

            # If an operation fails inside a batch,
            # restore all balances.
            if batch_active and batch_backup is not None:

                for account_id, old_balance in batch_backup.items():
                    bank.accounts[account_id]._balance = old_balance

                failed_batches += 1

                # Ignore remaining operations until BATCH_END
                while True:
                    try:
                        remaining = input().strip()

                        if remaining == "BATCH_END":
                            break
                    except EOFError:
                        break

                batch_active = False
                batch_backup = None

    # Print final balances in account ID order
    for account_id in sorted(bank.accounts):
        print(
            account_id,
            bank.accounts[account_id].balance
        )

    if failed_batches > 0:
        print("FAILED", failed_batches)


if __name__ == "__main__":
    main()