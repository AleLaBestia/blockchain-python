import functools
import hashlib as hl
import json
from collections import OrderedDict
import pickle
from hash_util import hash_string_256, hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'max'
participants = {'max'}


def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            global blockchain
            global open_transactions
            updated_blockchain = []

            blockchain = json.loads(file_content[0][:-1])
            for block in blockchain:
                converted_tex = [Transaction(
                    tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(
                    block['index'], block['previous_hash'], converted_tex, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(
                    tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):

        genesis_block = Block(0, '', [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []


load_data()


def save_data():
    with open('blockchain.txt', mode='w') as f:
        saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp)
                                                       for block_el in blockchain]]
        f.write(json.dumps(saveable_chain))
        f.write('\n')
        saveable_tx = [tx.__dict__ for tx in open_transactions]
        f.write(json.dumps(saveable_tx))


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions
                  if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount
                      for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx.amount for tx in block.transactions
                     if tx.recipient == participant] for block in blockchain]

    amount_received = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_received-amount_sent


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1):
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()

    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your amount: '))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input('your choice: ')
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print('outputting block')
        print(block)
    else:
        print('-'*20)


waiting_for_input = True

while waiting_for_input:
    print('please choose')
    print('1: add new transaction')
    print('2: mine a block')
    print('3: outut blocks')
    print('4: Output participants')
    print('5: check transaction validity')
    print('q:quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print(open_transactions)
        else:
            print('transaction failed')
            print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        verifier = Verification()
        if verifier.verify_transactions(get_balance, open_transactions):
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('input invalid')
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print('invalid blockchain')
        break


print('Done!')
