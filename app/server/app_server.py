from flask import Flask, jsonify, request
import p2pseed_pb2
import p2pseed_pb2_grpc
import grpc
import sqlite3
import blockchain_pb2
import blockchain_pb2_grpc
from tx import *
from record import *
import random
import string
import json

class server:
    def __init__(self):
        self.onlinenode = []
        self.wallet = 5
        # init_sql()

    def getNode(self):
        with grpc.insecure_channel('127.0.0.1:50050') as channel:
            stub = p2pseed_pb2_grpc.P2pSeedStub(channel)
            tran_msg = "sender is connected"
            response = stub.FindOnlineNode(p2pseed_pb2.FindOnlineNodeRequest(message=tran_msg))
            self.onlinenode.clear()
            for port in response.port:
                self.onlinenode.append(int(port))


def prt_sql():
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute(
        "select * from USER order by ID asc;")
    columns_tuple = c.fetchall()
    print(columns_tuple)

    conn.commit()
    conn.close()
    return columns_tuple


# 0-没找到 1-医生 2-患者
def search_sql(id, pw) -> int:
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute(
        "select * from USER;")
    columns_tuple = c.fetchall()
    for row in columns_tuple:
        if row[0] == id and row[1] == pw:
            if row[2] == 'doctor':
                return 1
            else:
                return 2
    conn.commit()
    conn.close()
    return 0


def search_user_sql(id) -> bool:
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute(
        "select * from USER where ID=?;", (id,))
    columns_tuple = c.fetchall()
    conn.commit()
    conn.close()
    if len(columns_tuple) != 0:
        return False
    return True


def init_sql():  # 初始化数据库
    con = sqlite3.connect('user_info.db')
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS USER(ID TEXT NOT NULL,PASSWORD TEXT NOT NULL,AUTHORITY NOT NULL);")  # 创立用户表
    con.commit()
    con.close()


def ins_sql(id, password, auth):  # 加入账号
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("INSERT INTO USER(ID,PASSWORD,AUTHORITY) \
         VALUES (?,?,?)", (id, password, auth))
    conn.commit()
    conn.close()


def del_sql(id):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("DELETE FROM USER WHERE ID=?", (id,))
    conn.commit()
    conn.close()


server = server()
app = Flask(__name__)

@app.route("/query", methods=['POST'])
def queryRecordName():
    info = request.values.get("Info")
    method = request.values.get("Method")
    server.getNode()
    record = []
    for node in server.onlinenode:
        with grpc.insecure_channel('127.0.0.1:' + str(node)) as channel:
            stub = blockchain_pb2_grpc.BlockChainStub(channel)
            try:
                response = stub.QueryBlockchain(blockchain_pb2.QueryBlockchainRequest(message='hello'))
            except Exception:
                continue
            else:
                if method == '2':
                    for block in response.blocks:
                        for tx in block.transaction:
                            txjson = eval(tx.data)
                            if txjson['RecordId'] == str(info):
                                record.append(txjson)
                elif method == '1':
                    for block in response.blocks:
                        for tx in block.transaction:
                            txjson = eval(tx.data)
                            if txjson['PatientName'] == str(info):
                                record.append(txjson)
    if len(record) != 0:
        response = {
            "message":"successful",
            "record":record
        }
    else:
        response = {
            "message": "fail",
            "record": ""
        }
    return jsonify(response),200


@app.route("/halo", methods=['GET'])
def Hello():
    response = {
        "message": "halo!"
    }
    return jsonify(response), 200


@app.route("/login", methods=['POST'])
def validLogin():
    id = request.values.get("userId")
    pw = request.values.get("passWord")
    state = search_sql(id, pw)
    response = {
        "message": "",
        "authority": ""
    }
    if state == 0:
        response = {
            "message": "fail",
            "authority": "None"
        }
    elif state == 1:
        response = {
            "message": "successful",
            "authority": "doctor"
        }
    elif state == 2:
        response = {
            "message": "successful",
            "authority": "patient"
        }

    return jsonify(response), 200


@app.route("/sign", methods=['POST'])
def signUp():
    u = request.values.get("userId")
    p = request.values.get("passWord")
    response = {
        "message": ""
    }
    if search_user_sql(u) == False:
        response = {
            "message": "fail"
        }

    else:
        ins_sql(u, p, "patient")
        response = {
            "message": "successful"
        }

    return jsonify(response), 200

@app.route("/recharge", methods=['POST'])
def addWallet():
    tar = request.values.get("value")
    server.wallet += int(tar)
    response={
        "message": "successful",
        "balance": str(server.wallet)
    }
    return response

@app.route("/sendtx", methods=['POST'])
def sendTX():
    server.getNode()
    sender = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    receiver = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    amount = 1
    p = request.values.get("PatientName")
    i = request.values.get("In_time")
    o = request.values.get("Out_time")
    f = request.values.get("Fee")
    nR = newRecord(p, i, o, f)
    id = nR.id
    data = str(nR.toJson())
    for node in server.onlinenode:
        with grpc.insecure_channel('127.0.0.1:' + str(node)) as channel:
            stub = blockchain_pb2_grpc.BlockChainStub(channel)
            try:
                tx = blockchain_pb2.Transaction(sender=sender, receiver=receiver,
                                                amount=int(amount), data=data)
                response = stub.AddTransaction(blockchain_pb2.AddTransactionRequest(transaction=tx))
            except Exception:
                #   QMessageBox.about(self, 'error', 'the port can not connect')
                continue
            else:
                if server.wallet - amount >= 0:
                    print(response.message)
                    response = {
                        'message': 'success send the record',
                        'recordId': id
                    }
                    server.wallet -= amount  # 扣费
                else:
                    response = {
                        "message": "fail!",
                    }
    return jsonify(response), 200


if __name__ == '__main__':
    port = 5001
    app.run(host='127.0.0.1', port=port, debug=True)
