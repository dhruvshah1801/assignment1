import csv
from datetime import datetime


def validate_timestamp(timestamp):
    """Check whether timestamp follows ISO-like format."""
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False


def process_csv(filename):
    balances = {}

    credit_file = "credit.csv"
    debit_file = "debit.csv"
    error_file = "error.csv"

    with open(filename, "r", newline="") as infile:
        reader = csv.reader(infile)

        header = next(reader, None)

        with open(credit_file, "w", newline="") as cf, \
             open(debit_file, "w", newline="") as df, \
             open(error_file, "w", newline="") as ef:

            credit_writer = csv.writer(cf)
            debit_writer = csv.writer(df)
            error_writer = csv.writer(ef)

            # Write headers
            if header:
                credit_writer.writerow(header)
                debit_writer.writerow(header)
                error_writer.writerow(header + ["error"])

            for row in reader:

                try:
                    # Validate number of fields
                    if len(row) != 5:
                        raise ValueError("Invalid number of fields")

                    transaction_id = row[0].strip()
                    account_id = row[1].strip()
                    trans_type = row[2].strip().upper()
                    amount_text = row[3].strip()
                    timestamp = row[4].strip()

                    # Validate required fields
                    if not transaction_id or not account_id:
                        raise ValueError("Missing transaction/account ID")

                    # Validate transaction type
                    if trans_type not in ("CREDIT", "DEBIT"):
                        raise ValueError("Invalid transaction type")

                    # Validate amount
                    try:
                        amount = float(amount_text)
                    except ValueError:
                        raise ValueError("Amount is not numeric")

                    if amount <= 0:
                        raise ValueError("Amount must be positive")

                    # Validate timestamp
                    if not validate_timestamp(timestamp):
                        raise ValueError("Invalid timestamp")

                    # Valid row
                    clean_row = [
                        transaction_id,
                        account_id,
                        trans_type,
                        amount_text,
                        timestamp
                    ]

                    if trans_type == "CREDIT":
                        credit_writer.writerow(clean_row)

                        balances[account_id] = (
                            balances.get(account_id, 0) + amount
                        )

                    else:
                        debit_writer.writerow(clean_row)

                        balances[account_id] = (
                            balances.get(account_id, 0) - amount
                        )

                except Exception as e:
                    error_writer.writerow(row + [str(e)])

    # Sort by descending absolute balance change
    sorted_balances = sorted(
        balances.items(),
        key=lambda x: (-abs(x[1]), x[0])
    )

    for account, balance in sorted_balances:
        if balance.is_integer():
            balance = int(balance)

        print(account, balance)

    print("Files created: credit.csv, debit.csv, error.csv")


def main():
    filename = input().strip()

    try:
        process_csv(filename)

    except FileNotFoundError:
        print("ERROR: Input file not found")

    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    main()