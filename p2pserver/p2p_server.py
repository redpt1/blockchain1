import p2pseed_pb2
import p2pseed_pb2_grpc
import sys
import grpc
from concurrent import futures
import logging


class P2pSendServer(p2pseed_pb2_grpc.P2pSeedServicer):
    def __init__(self):
        self.allnode = []

    def Hello(self, request, context):
        response = p2pseed_pb2.HelloResponse()
        response.message = 'successfully connect to the seed server'
        print('from',request.port)
        if request.port not in self.allnode:
            self.allnode.append(request.port)
        for node in self.allnode:
            response.port.append(node)
        print("all node:[")
        for node in self.allnode:
            print(node)
        print("]")

        return response

    def FindOnlineNode(self, request, context):
        response = p2pseed_pb2.FindOnlineNodeResponse()
        print(request.message)
        for online in self.allnode:
            response.port.append(online)
        return response

def serve(port=50050):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    try:
        p2pseed_pb2_grpc.add_P2pSeedServicer_to_server(P2pSendServer(), server)
        server.add_insecure_port('127.0.0.1:' + str(port))
    except RuntimeError:
        print("Error: the port is occupied")
        return
    else:
        server.start()
        print("seed server started, listening on " + str(port))

    server.wait_for_termination()


# run the server
if __name__ == '__main__':
    logging.basicConfig()
    index = len(sys.argv)
    if index == 2:
        serve(port=int(sys.argv[1]))
    else:
        serve()
