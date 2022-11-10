import time
from ui.txsender import Ui_MainWindow
from PySide2.QtWidgets import *
import grpc
import blockchain_pb2
import blockchain_pb2_grpc
import p2pseed_pb2
import p2pseed_pb2_grpc
import random

class TxSender(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.onlinenode = []
        self.sender = ''
        self.receiver = ''
        self.amount = ''

        self.ui.pushButton.clicked.connect(self.sendTx)

    def setPort(self):
        with grpc.insecure_channel('127.0.0.1:50050') as channel:
            stub = p2pseed_pb2_grpc.P2pSeedStub(channel)
            tran_msg = "sender is connected"
            response = stub.FindOnlineNode(p2pseed_pb2.FindOnlineNodeRequest(message=tran_msg))
            self.onlinenode.clear()
            for port in response.port:
                self.onlinenode.append(int(port))


    def sendTx(self):
        self.setPort()
        self.sender = self.ui.lineEdit.text()
        self.receiver = self.ui.lineEdit_2.text()
        self.amount = self.ui.lineEdit_3.text()

        if len(self.sender) and len(self.receiver) and len(self.amount):
            for node in self.onlinenode:
                with grpc.insecure_channel('127.0.0.1:' + str(node)) as channel:
                    stub = blockchain_pb2_grpc.BlockChainStub(channel)
                    try:
                        tx = blockchain_pb2.Transaction(sender=self.sender, receiver=self.receiver,
                                                        amount=int(self.amount),data='hello')
                        response = stub.AddTransaction(blockchain_pb2.AddTransactionRequest(transaction=tx))
                    except Exception:
                     #   QMessageBox.about(self, 'error', 'the port can not connect')
                        continue
                    else:
                        print(response.message)
        else:
            QMessageBox.about(self,'error','can not be null')



if __name__ == '__main__':
    app = QApplication([])
    window = TxSender()
    window.setWindowTitle('sender')
    window.show()
    app.exec_()
