import time
import hashlib
class Record:
    def __init__(self,p,i,o,f):
        self.patientName = p
        self.in_time = i
        self.out_time = o
        self.fee = f
        self.id = hashlib.sha1((str(time.time())+p+i+o+f).encode("utf-8")).hexdigest()


    def toJson(self):
        return{
            'PatientName': self.patientName,
            'In_time': self.in_time,
            'Out_time': self.out_time,
            'Fee': self.fee,
            'RecordId': self.id
        }

def newRecord(p,i,o,f) -> Record:
    record = Record(p,i,o,f)
    return record