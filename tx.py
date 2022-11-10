class Transaction:
    def __init__(self):
        self.sender=''
        self.receiver=''
        self.amount=0
        self.data=''

    def toJsonStr(self):
        return {
            'sender':self.sender,
            'receiver':self.receiver,
            'amount':self.amount,
            'data':self.data
        }

def NewTransaction(sender,receiver,amount,data):
    new_transaction = Transaction()
    new_transaction.sender = sender
    new_transaction.receiver = receiver
    new_transaction.amount = amount
    new_transaction.data = data
    return new_transaction