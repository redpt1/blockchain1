import hashlib
import random
from tx import *
import time
from typing import List


class Block:
    def __init__(self):
        self.Index = 0
        # 用于计算hash pow
        self.Timestamp = int(time.time())
        self.Nonce = 0
        # 通过TX计算自身hash
        self.Hash = ''
        self.PrevBlockHash = ''
        self.Merkle_tree = ''
        self.Transaction = []

    def merkleTree(self) :
        hash = ''
        if len(self.Transaction) != 0:

            for tx in self.Transaction:
                hash += hashlib.sha1(str(tx.toJsonStr()).encode("utf-8")).hexdigest()

            hash = hashlib.sha1(str(hash).encode("utf-8")).hexdigest()

        self.Merkle_tree=hash

class Blockchain:
    def __init__(self):
        self.blocks = []

        genesis_block = NewBlock(0, [], '', 0)  # 创世区块
        self.blocks.append(genesis_block)
        self.target_hash = 1


# function of create a new block
def NewBlock(index: int, transaction: List, prevBlockHash: str, nonce: int):
    # new block hash (address) generation should include the previous block's hash
    hash_code = ''
    for tx in transaction:
        hash_code += tx.toJsonStr()
    hash_code += prevBlockHash
    hash = hashlib.sha1(hash_code.encode("utf-8")).hexdigest()
    # declare a block with Block class
    block = Block()
    block.Index = index
    block.Hash = hash
    block.Transaction = transaction
    block.PrevBlockHash = prevBlockHash
    block.Nonce = nonce
    return block


# function of append a new block with the blockchain
def AddBlock(blockchain: Blockchain, transaction: str, expect_hash: int):
    # if the miner give the correct puzzle answer (target_hash), then the miner's transaction will be accepted and added at new block
    if expect_hash == blockchain.target_hash:
        prevBlockHash = blockchain.blocks[-1].Hash
        block = NewBlock(transaction=transaction, prevBlockHash=prevBlockHash)
        blockchain.blocks.append(block)
        # Describe the status at terminal
        print("Blockchain updated: ")
        for i in range(len(blockchain.blocks)):
            print("block " + str(i) + ":")
            print('block hash = ' + blockchain.blocks[i].Hash)
            print('block transaction = ' + blockchain.blocks[i].Transaction)
        print()
        blockchain.target_hash = random.randint(0, 9)
        print("Next Block's Puzzle Hash is " + str(blockchain.target_hash))
        return blockchain.blocks[-1].Hash
    # if the miner give the wrong puzzle answer, return false.
    else:
        return "False"


# Encapsulate the function of creating a blockchain into NewBlockchain
def NewBlockchain():
    new_blockchain = Blockchain()
    return new_blockchain
