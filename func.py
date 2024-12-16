import secrets

tokens = {}
user_ids = {}
transactions = {}

def create_token(user_id, username, bot):
    token = secrets.token_hex(16)
    tokens[username] = token
    user_ids[username] = user_id
    return token


def update_transaction(user_transactions, target_username, amount):
    for i, transaction in enumerate(user_transactions):
        if transaction['username'] == target_username:
            transaction['amount'] += amount
            if transaction['amount'] == 0:
                user_transactions.remove(transaction)
                return -100
            return True
    return False


def add_transaction(user_id, username, amount):
    if user_id not in transactions:
        transactions[user_id] = []
    if username not in transactions:
        transactions[username] = []

    success_transaction1 = update_transaction(transactions[user_id], username, amount)
    success_transaction2 = update_transaction(transactions[username], user_id, -amount)

    if success_transaction2 == -100 or success_transaction1 == -100:
        return False

    if not success_transaction1 and amount != 0:
        transactions[user_id].append({"username": username, "amount": amount})
    if not success_transaction2 and amount != 0:
        transactions[username].append({"username": user_id, "amount": -amount})

    return True


def get_user_transactions(user_id):
    user_transactions = transactions.get(user_id, [])

    return user_transactions
