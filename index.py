blockchain = []
open_transactions = []
owner = 'max'


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1):
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}

    open_transactions.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    block = {
        'previous_hash': 'ydyd',
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)


def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your amount: '))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input('your choice: ')


def print_blockchain_elements():
    for block in blockchain:
        print('outputting block')
        print(block)


def verify_chain():
    block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            block_index += 1
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break

    return is_valid


waiting_for_input = True

while waiting_for_input:
    print('please choose')
    print('1: add new')
    print('2:outut blocks')
    print('h: Manipulate the chain')
    print('q:quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('input invalid')

    if not verify_chain():
        print('invalid blockchain')
        break


print('Done!')
