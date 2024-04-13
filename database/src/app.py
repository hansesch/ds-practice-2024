import grpc
import sys
import os
from concurrent import futures

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path)

import database_pb2 as database
import database_pb2_grpc as database_grpc


class DatabaseService(database_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.data = {
            'Book 1': 3,
            'Book 2': 4
        }

    def Read(self, request: database.ReadRequest, context):
        if request.title in self.data:
            return database.ReadResponse(stockValue=self.data[request.title])
        else:
            return database.ReadResponse(stockValue=0)
    
    def Write(self, request: database.WriteRequest, context):
        self.data[request.title] = request.stockValue
        return database.WriteResponse(isSuccess=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    database_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    port = "50057"
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()