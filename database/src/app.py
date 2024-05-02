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
        self.write_order_statuses = dict()
        self.decrement_order_statuses = dict()

    def get_lock(self, id):
        if id not in self.locks:
            self.locks[id] = threading.Lock()
        return self.locks[id]
    
    def Read(self, request: database.ReadRequest, context):
        # If the book is locked, wait until it is unlocked for reading
        while request.id in self.locks and self.locks[request.id].locked():
            time.sleep(1)
        # Attempt to read from the last instance in the chain (tail), when it fails, remove it from the list and try the next from last    
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
    
    # PrepareWrite and CommitWrite are used to prepare and commit write operations
    def PrepareWrite(self, request: database.PrepareWriteRequest, context):
        if request.id in self.write_order_statuses:
            print(f"Write operation for order {request.id} cannot be prepared because it is already in state {self.write_order_statuses[request.id]['status']}")
            return database.PrepareResponse(isReady=False)
        
        self.write_order_statuses[request.id] = {
            'status': 'ready',
            'stockValue': request.stockValue
        }
        return database.PrepareResponse(isReady=True)
    
    # First check if the write operation has been prepared and not already completed, then call the Write method
    def CommitWrite(self, request: database.CommitRequest, context):
        if request.id not in self.write_order_statuses:
            print(f"Write operation for order {request.id} cannot be commited because it has not been prepared")
            return database.CommitResponse(isSuccess=False)
        elif self.write_order_statuses[request.id]['status'] == 'completed':
            print(f"Write operation for order {request.id} cannot be commited because it has already been completed")
            return database.CommitResponse(isSuccess=False)
        self.Write(request.id, self.write_order_statuses[request.id]['stockValue'])
        
    # Write method is used to write the stock value to the database
    # It forwards the write request to the head of the chain
    # If the call fails, it removes the failed port from the list and retries the next on the list    
    def Write(self, orderId, stockValue):
        with self.get_lock(orderId):
            while self.hosts:
                try:
                    # Attempt to forward the write request to the head of the chain
                    with grpc.insecure_channel(f'{self.hosts[0]}:{self.ports[0]}') as channel:
                        stub = databaseinstance_grpc.DatabaseInstanceServiceStub(channel)
                        response: databaseinstance.WriteResponse = stub.Write(databaseinstance.WriteRequest(id=orderId, stockValue=stockValue, hosts=self.hosts[1:], ports=self.ports[1:]))
                        if response.isSuccess:
                            return database.CommitResponse(isSuccess=True)
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

    # PrepareDecrementStock checks if the decrement operation can be prepared and prepares it
    def PrepareDecrementStock(self, request: database.PrepareDecrementStockRequest, context):
        if request.id in self.decrement_order_statuses:
            print(f"Decrement operation for order {request.id} cannot be prepared because it is already in state {self.decrement_order_statuses[request.id]['status']}")
            return database.PrepareResponse(isReady=False)
        
        self.decrement_order_statuses[request.id] = {
            'status': 'ready',
            'decrement': request.decrement
        }
        return database.PrepareResponse(isReady=True)

    # CommitDecrementStock checks if the decrement operation can be committed and commits it
    def CommitDecrementStock(self, request: database.CommitRequest, context):
        if request.id not in self.decrement_order_statuses:
            print(f"Decrement operation for order {request.id} cannot be commited because it has not been prepared")
            return database.CommitResponse(isSuccess=False)
        elif self.decrement_order_statuses[request.id]['status'] == 'completed':
            print(f"Decrement operation for order {request.id} cannot be commited because it has already been completed")
            return database.CommitResponse(isSuccess=False)
        
        decrement_value = self.decrement_order_statuses[request.id]['decrement']
        print(f"Decrement stock request received for ID {request.id}, decrementing by {decrement_value}.")
        current_value = self.Read(database.ReadRequest(id=request.id), context)
        new_stock_value = current_value.stockValue - decrement_value
        self.Write(request.id, new_stock_value)
        return database.CommitResponse(isSuccess=True)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    database_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    port = "50057"
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()