import grpc
import sys
import os
from concurrent import futures
import threading
import time

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/databaseinstance'))
sys.path.insert(1, utils_path)

import database_pb2 as database
import database_pb2_grpc as database_grpc
import databaseinstance_pb2 as databaseinstance
import databaseinstance_pb2_grpc as databaseinstance_grpc


class DatabaseService(database_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.hosts = ["databaseinstance1", "databaseinstance2", "databaseinstance3", "databaseinstance4"]
        self.ports = ["50045", "50046", "50047", "50048"]
        self.locks = {}

    def get_lock(self, id):
        if id not in self.locks:
            self.locks[id] = threading.Lock()
        return self.locks[id]
    
    def Read(self, request: database.ReadRequest, context):
        while request.id in self.locks and self.locks[request.id].locked():
            time.sleep(1)
        while self.hosts:
            try:
                with grpc.insecure_channel(f'{self.hosts[-1]}:{self.ports[-1]}') as channel:
                    stub = databaseinstance_grpc.DatabaseInstanceServiceStub(channel)
                    response = stub.Read(request)
                    return database.ReadResponse(stockValue=response.stockValue)
            except grpc.RpcError as e:
                print(f"Failed to connect to tail databaseinstance:{self.hosts[-1]}:{self.ports[-1]}. Removing from list.")
                self.ports.pop()
                self.hosts.pop()
        raise Exception("All database instances are down.")
    
    def Write(self, request: database.WriteRequest, context):
        with self.get_lock(request.id):
            while self.hosts:
                try:
                    # Attempt to forward the write request to the head of the chain
                    with grpc.insecure_channel(f'{self.hosts[0]}:{self.ports[0]}') as channel:
                        stub = databaseinstance_grpc.DatabaseInstanceServiceStub(channel)
                        response = stub.Write(databaseinstance.WriteRequest(id=request.id, stockValue=request.stockValue, hosts=self.hosts[1:], ports=self.ports[1:]))
                    if response.isSuccess:
                        return database.WriteResponse(isSuccess=True)
                    else:
                        print(f"Failed to connect to databaseinstance:{response.failedhost}:{response.failedport}. Removing from list.")
                        # If the call fails, remove the failed port from the list and retry
                        self.hosts.remove(response.failedhost)
                        self.ports.remove(response.failedport)
                except grpc.RpcError as e:
                    # If the call fails, remove the failed port from the list and retry
                    print(f"Failed to connect to the head database instance:{self.hosts[0]}:{self.ports[0]}. Removing from list.")
                    self.ports.pop(0)
                    self.hosts.pop(0)
            # If all instances fail, raise an exception
            raise Exception("All database instances are down.")


    def DecrementStock(self, request: database.DecrementStockRequest, context):
        print(f"Decrement stock request received for ID {request.id}, decrementing by {request.decrement}.")
        current_value = self.Read(database.ReadRequest(id=request.id), context)
        new_stock_value = current_value.stockValue - request.decrement
        self.Write(database.WriteRequest(id=request.id, stockValue=new_stock_value), context)
        return database.DecrementStockResponse(isSuccess=True)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    database_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    port = "50057"
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()