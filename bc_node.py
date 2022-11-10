import random
from concurrent import futures
import logging
import grpc
import blockchain_pb2
import blockchain_pb2_grpc
import p2pseed_pb2_grpc
import p2pseed_pb2
from node import *
from block import *
import sys

# python bc_retainer.py 50051
# We implement the function at server class
class BlockchainServer(blockchain_pb2_grpc.BlockChainServicer):
    # When the server created, a new blockchain will be created too
    def __init__(self, port):
        self.node = NewNode()
        self.node.setPort(port)
        self.LoginSeed()
        if len(self.node.neighbor) > 1:
            self.Consensus()

        # 初始化时取得最长链

    def Consensus(self):
        flag = 0
        for neighbor in self.node.neighbor:
            if neighbor != self.node.port:
                with grpc.insecure_channel('127.0.0.1:' + str(neighbor)) as channel:
                    stub = blockchain_pb2_grpc.BlockChainStub(channel)
                    # 连通性检测
                    try:
                        response = stub.QueryBlockchain(
                            blockchain_pb2.QueryBlockchainRequest(
                                message='node' + str(self.node.port) + 'apply to query the blockchain'))
                    except Exception:
                        print("同步过程" + str(neighbor) + "节点已下线")
                        continue
                    else:
                        if response:
                            if len(response.blocks) > len(self.node.blockchain.blocks):  # 长度不够，就更新并验证链
                                flag = neighbor
                                if self.CheckBlockChain(response):
                                    self.node.blockchain.blocks.clear()
                                    for block in response.blocks:
                                        newBlock = Block()
                                        newBlock.Index = block.index
                                        newBlock.Timestamp = block.timestamp
                                        newBlock.Nonce = block.nonce
                                        newBlock.Hash = block.hash
                                        newBlock.PrevBlockHash = block.prevBlockHash
                                        newBlock.Merkle_tree = block.merkle_tree
                                        for tx in block.transaction:
                                            newTx = NewTransaction(tx.sender, tx.receiver, tx.amount, tx.data)
                                            newBlock.Transaction.append(newTx)
                                        self.node.blockchain.blocks.append(newBlock)
        if flag != 0:
            print("获取最长链,from: ", flag)

    def LoginSeed(self):
        with grpc.insecure_channel('127.0.0.1:50050') as channel:
            stub = p2pseed_pb2_grpc.P2pSeedStub(channel)
            response = stub.Hello(p2pseed_pb2.HelloRequest(message='apply to connect', port=self.node.port))
            for nodes in response.port:
                if nodes not in self.node.neighbor:
                    self.node.addNeighbor(nodes)
            print(str(self.node.port) + " 正在与其他node连接")
            for nodes in self.node.neighbor:
                if nodes != self.node.port:
                    with grpc.insecure_channel('127.0.0.1:' + str(nodes)) as channel:
                        stub = blockchain_pb2_grpc.BlockChainStub(channel)
                        # 连通性检测
                        try:
                            response = stub.AddNeighbor(
                                blockchain_pb2.AddNeighborRequest(message='apply to connect', port=self.node.port))
                        except Exception:
                            print(str(nodes) + "节点已下线")
                            continue
                        else:
                            print(response.message)

    def AddNeighbor(self, request, context):
        response = blockchain_pb2.AddNeighborResponse()
        print('from:' + str(request.port) + request.message)
        if not (request.port in self.node.neighbor):
            self.node.neighbor.append(request.port)
            response.message = 'connect to' + str(self.node.port) + 'successfully'
        else:
            response.message = 'has already connected to' + str(self.node.port)

        return response

    def AddBlock(self, request, context):
        hash_code = AddBlock(self.node.blockchain, request.transaction, request.expectHash)
        return blockchain_pb2.AddBlockResponse(hash=hash_code)

    def QueryBlockchain(self, request, context):
        response = blockchain_pb2.QueryBlockchainResponse()
        for block in self.node.blockchain.blocks:
            pb2_block = blockchain_pb2.Block()
            for tx in block.Transaction:
                tx1 = blockchain_pb2.Transaction(sender=tx.sender, receiver=tx.receiver, amount=int(tx.amount),
                                                 data=tx.data)
                pb2_block.transaction.append(tx1)
            pb2_block.index = block.Index
            pb2_block.timestamp = block.Timestamp
            pb2_block.nonce = block.Nonce
            pb2_block.hash = block.Hash
            pb2_block.prevBlockHash = block.PrevBlockHash
            pb2_block.merkle_tree = block.Merkle_tree
            response.blocks.append(pb2_block)
        return response

    # For step 3
    def QueryBlock(self, request, context):
        response = blockchain_pb2.QueryBlockResponse()

        ans = self.node.blockchain.blocks[-1]
        response.block.transaction = ans.Transaction
        response.block.hash = ans.Hash
        response.block.prevBlockHash = ans.PrevBlockHash
        # message 单独赋值
        return response

    def PrintBlockInfo(self, block: Block):
        info = {}
        info['index'] = block.Index
        info['timestamp'] = block.Timestamp
        info['nonce'] = block.Nonce
        info['prehash'] = block.PrevBlockHash
        info['merkle_tree'] = block.Merkle_tree
        info['hash'] = block.Hash
        allinfo = []
        allinfo.append(info)
        for tx in block.Transaction:
            tran = {}
            tran['sender'] = tx.sender
            tran['receiver'] = tx.receiver
            tran['amount'] = tx.amount
            tran['data'] = tx.data
            allinfo.append(tran)

        return allinfo

    def Broadcast(self, request, context):
        response = blockchain_pb2.BroadcastResponse()
        response.message = 'get the broadcast'
        if len(request.blocks) - 1 > self.node.blockchain.blocks[-1].Index:  # 长度不够，就更新并验证链
            if self.CheckBlockChain(request):
                self.node.blockchain.blocks.clear()
                for block in request.blocks:
                    newBlock = Block()
                    newBlock.Index = block.index
                    newBlock.Timestamp = block.timestamp
                    newBlock.Nonce = block.nonce
                    newBlock.Hash = block.hash
                    newBlock.PrevBlockHash = block.prevBlockHash
                    newBlock.Merkle_tree = block.merkle_tree
                    for tx in block.transaction:
                        newTx = NewTransaction(tx.sender, tx.receiver, tx.amount, tx.data)
                        newBlock.Transaction.append(newTx)
                    self.node.blockchain.blocks.append(newBlock)
        return response

    def BroadcastBC(self):
        for neighbor in self.node.neighbor:
            with grpc.insecure_channel('127.0.0.1:' + str(neighbor)) as channel:
                stub = blockchain_pb2_grpc.BlockChainStub(channel)
                # 连通性检测
                request = blockchain_pb2.BroadcastRequest()
                for block in self.node.blockchain.blocks:
                    block.merkleTree()
                    pb2_block = blockchain_pb2.Block()
                    for tx in block.Transaction:
                        tx1 = blockchain_pb2.Transaction(sender=tx.sender, receiver=tx.receiver,
                                                         amount=int(tx.amount), data=tx.data)
                        pb2_block.transaction.append(tx1)
                    pb2_block.index = block.Index
                    pb2_block.timestamp = block.Timestamp
                    pb2_block.nonce = block.Nonce
                    pb2_block.hash = block.Hash
                    pb2_block.prevBlockHash = block.PrevBlockHash
                    pb2_block.merkle_tree = block.Merkle_tree
                    request.blocks.append(pb2_block)
                try:
                    response = stub.Broadcast(request)
                except Exception:
                    # print(str(neighbor) + "节点已下线")
                    continue
            # else:
            # print(response.message)

    def AddTransaction(self, request, context):
        response = blockchain_pb2.AddTransactionResponse()
        tran = NewTransaction(request.transaction.sender, request.transaction.receiver, request.transaction.amount,
                              request.transaction.data)
        if self.node.blockchain.blocks[-1].Index == 0 or len(self.node.blockchain.blocks[-1].Transaction) == 2:
            self.Miner()
            self.node.blockchain.blocks[-1].Transaction.append(tran)

            print("加入新tx后区块状态")
            for block in self.node.blockchain.blocks:
                if block.Index != 0:
                    block.merkleTree()
                print(self.PrintBlockInfo(block))

        elif len(self.node.blockchain.blocks[-1].Transaction) < 2:  # 非创世区块
            self.BroadcastBC()
            self.node.blockchain.blocks[-1].Transaction.append(tran)
            print("加入新tx后区块状态")
            for block in self.node.blockchain.blocks:
                block.merkleTree()
                print(self.PrintBlockInfo(block))

        response.message = 'OK'
        return response

    def PoW(self, preblock: Block) -> Block:
        preblock.merkleTree()
        prehash = ''
        prehash += hashlib.sha1(preblock.PrevBlockHash.encode("utf-8")).hexdigest()
        prehash += hashlib.sha1(str(preblock.Timestamp).encode("utf-8")).hexdigest()
        prehash += hashlib.sha1(str(preblock.Merkle_tree).encode("utf-8")).hexdigest()
        prehash = hashlib.sha1(prehash.encode("utf-8")).hexdigest()
        nonce = 0
        target_hash = ''
        while True:
            target_hash = hashlib.sha1((str(prehash) + str(nonce)).encode("utf-8")).hexdigest()
            if str(target_hash)[0] == '0':
                break
            else:
                nonce += 1
        # print(nonce)
        preblock.Hash = str(target_hash)
        preblock.Nonce = nonce
        newblock = NewBlock(preblock.Index + 1, [], prehash, 0)
        return newblock

    def Miner(self):
        preblock = self.node.blockchain.blocks[-1]
        if len(preblock.Transaction) < 2 and preblock.Index != 0:  # 小于2不用生成区块
            return
        # print(preblock.Index,preblock.Transaction)
        # print('由node: '+str(self.node.port)+'达成,建立新块', preblock.Index + 1)
        newblock = self.PoW(preblock)
        self.node.blockchain.blocks.append(newblock)
        print("新建区块后状态")
        for block in self.node.blockchain.blocks:
            print(self.PrintBlockInfo(block))
        self.BroadcastBC()

    # todo 检查区块是否合法
    def CheckBlockChain(self, chain: blockchain_pb2.QueryBlockchainResponse or blockchain_pb2.BroadRequest) -> bool:
        preblock = chain.blocks[1]
        for block in chain.blocks[2:]:  # 除去创世区块
            prehash = ''
            prehash += hashlib.sha1(str(preblock.prevBlockHash).encode("utf-8")).hexdigest()
            prehash += hashlib.sha1(str(preblock.timestamp).encode("utf-8")).hexdigest()
            prehash += hashlib.sha1(str(preblock.merkle_tree).encode("utf-8")).hexdigest()
            prehash = hashlib.sha1(prehash.encode("utf-8")).hexdigest()
            target = hashlib.sha1((str(prehash) + str(preblock.nonce)).encode("utf-8")).hexdigest()
            if str(target)[0] != '0':
                return False
            preblock = block
        # print("++++++++++++++++++++++++ok+++++++++++++++++++")
        return True


# server setting
def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    try:
        blockchain_pb2_grpc.add_BlockChainServicer_to_server(BlockchainServer(port), server)
        server.add_insecure_port('127.0.0.1:' + str(port))
    except Exception:
        print("Error: the port is occupied")
        return
    else:
        print("blockchain started, listening on " + str(port))
        server.start()

    server.wait_for_termination()


# run the server
if __name__ == '__main__':
    logging.basicConfig()
    index = len(sys.argv)
    if index == 2:
        serve(port=int(sys.argv[1]))
    else:
        serve()
