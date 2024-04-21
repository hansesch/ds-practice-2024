import grpc
import sys
import os
from concurrent import futures

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/databaseinstance'))
sys.path.insert(0, utils_path)

import databaseinstance_pb2 as databaseinstance
import databaseinstance_pb2_grpc as databaseinstance_grpc


class DatabaseInstanceService(databaseinstance_grpc.DatabaseInstanceServiceServicer):
    def __init__(self):
        self.data = {
            "1": 7,
            "2": 15,
            "3": 15,
            "4": 15
        }

    def Read(self, request: databaseinstance.ReadRequest, context):
        print(f"Read request received for ID {request.id}, returning value {self.data[request.id]}.")
        return databaseinstance.ReadResponse(stockValue=int(self.data[request.id]))

    
    def Write(self, request: databaseinstance.WriteRequest, context):
        print(f"Write request received for ID {request.id}, new stock value {request.stockValue}.")
        current_value = self.data[request.id]
        self.data[request.id] = request.stockValue
        if request.ports:
            next_host = request.hosts.pop(0)
            next_port = request.ports.pop(0)
            try:
                with grpc.insecure_channel(f'{next_host}:{next_port}') as channel:
                    stub = databaseinstance_grpc.DatabaseInstanceServiceStub(channel)
                    response = stub.Write(databaseinstance.WriteRequest(id=request.id, stockValue=request.stockValue, hosts=request.hosts, ports=request.ports))
                    if not response.isSuccess:
                        #rollback
                        print(f"Rolling back {request.id} value to {current_value} from new value {request.stockValue} due to failed write request forward.")
                        self.data[request.id] = current_value
                    return response    
            except grpc.RpcError as e:
                print(f"Write request forward failed to: {next_host}:{next_port}.")
                # If the call fails, return a failure response with the failed port + host
                return databaseinstance.WriteResponse(isSuccess=False, failedhost=next_host, failedport=next_port)
        else:
            print("No port to forward to, I am the tail, returning writeResponse.")
            return databaseinstance.WriteResponse(isSuccess=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    databaseinstance_grpc.add_DatabaseInstanceServiceServicer_to_server(DatabaseInstanceService(), server)
    port = os.environ.get("PORT", 5000)
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()