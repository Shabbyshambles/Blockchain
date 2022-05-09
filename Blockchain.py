import hashlib
import json
from textwrap import dedent
from uuid import uuid4
#import jsonpickle
#from flask import Flask
from urllib.parse import urlparse
#from Crypto.PublicKey import RSA
#from Crypto.Signature import *
from time import time
from datetime import datetime
#import requests

class Blockchain (object):
    def __init__(self):
        self.chain = [self.addGenesisBlock()]
        self.pendingTransactions = []
        self.difficulty = 3
        self.minerRewards = 50
        self.blockSize = 10

    def generateKeys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)

        public_key = key.publickey().export_key()
        file_out = open("reciever.pem", "wb")
        file_out.write(public_key)

        return key.publickey.export_key().decode("ASCII")

    def minePendingTransactions(self, miner):
        lenPT = len(self.pendingTransactions)
        #if(lenPT<= 1):
        #    print("Not enough transactions to mine!")
        #    return False
        #else:
        for i in range(0, lenPT, self.blockSize):
            end = i+ self.blockSize
            if i >=lenPT:
                end = lenPT
            
            transactionSlice = self.pendingTransactions[i:end]

            newBlock = Block(transactionSlice, time(), len(self.chain))
            hashVal = self.getLastBlock().hash
            newBlock.prev = hashVal
            newBlock.mineBlock(self.difficulty)
            self.chain.append(newBlock)
        print("Mining Transactions Success")

    def getLastBlock(self):
        return self.chain[-1]


    def addBlock(self, block):
        if(len(self.chain) > 0):
            block.prev = self.getLastBlock().hash
        else:
            block.prev = None
        self.chain.append(block)

    def addGenesisBlock(self):
        tArr = []
        tArr.append(Transaction("me", "you", 10))
        genesis = Block(tArr, time(), 0)
        genesis.prev = "None"
        return genesis

    def chainJSONencode(self):

        blockArrJSON = []
        for block in self.chain:
            blockJSON={}
            blockJSON['hash'] = block.hash
            blockJSON['prev'] = block.prev
            
            transactionJSON = []
            blockArrJSON.append(blockJSON)
        return blockArrJSON
    
class Block (object):
    def __init__(self, transactions, time, index):
        self.index = index
        self.transactions = transactions
        self.prev = ' '
        self.nonse = 0
        self.time = time
        self.hash = self.calculateHash()

    def mineBlock(self, difficulty):
        arr = []
        for i in range(0, difficulty):
            arr.append(i)

        arrStr = map(str, arr)
        hashPuzzle = " ".join(arrStr)

        while self.hash[0:difficulty] !=hashPuzzle:
            self.nonse += 1
            self.hash = self.calculateHash()
            print("nonse: ", self.nonse)
            print("Hash Attempt: ", self.hash)
            print(" ")
        print(" ")
        print("Block Mined! Nonse to Solve Proof of Work: "+ self.nonse)
        return True



    def calculateHash(self):
        hashTransactions = " "
        for transaction in self.transactions:
            hashTransactions += transaction.hash

        hashString = str(self.time) + hashTransactions + self.prev + str(self.index)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()

class Transaction (object):
	def __init__(self, sender, reciever, amt):
		self.sender = sender;
		self.reciever = reciever;
		self.amt = amt;
		self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S"); #change to current date
		self.hash = self.calculateHash();

    def signTransaction(self, key, senderKey):
        if(self.hash != self.calculateHash()):
            print("transaction tampered error")
            return False
        if(str(key.publickey().export_key()) != ):



	def calculateHash(self):
		hashString = self.sender + self.reciever + str(self.amt) + str(self.time);
		hashEncoded = json.dumps(hashString, sort_keys=True).encode();
		return hashlib.sha256(hashEncoded).hexdigest();