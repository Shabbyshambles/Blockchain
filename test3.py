from Blockchain import Blockchain, Transaction, Block
from time import time
import pprint

pp = pprint.PrettyPrinter(indent = 4)

blockchain = Blockchain()
transaction = Transaction("Hugh G. Rection", "Rat Ass Moses", 10)

blockchain.pendingTransactions.append(transaction)

blockchain.minePendingTransactions("Nang")

pp.pprint(blockchain.chainJSONencode())
print("Length", len(blockchain.chain))