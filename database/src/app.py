import grpc
import sys
import os
from concurrent import futures
import redis 

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path)

import database_pb2 as database
import database_pb2_grpc as database_grpc


class DatabaseService(database_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.redis_clients = [
            redis.Redis(host='redis1', port=6379, db=0),
            redis.Redis(host='redis2', port=6380, db=0),
            redis.Redis(host='redis3', port=6381, db=0)
        ]

    def Read(self, request: database.ReadRequest, context):
        value = self.redis_clients[0].get(request.title)
        if value is not None:
            return database.ReadResponse(stockValue=int(value))
        else:
            return database.ReadResponse(stockValue=0)
    
    def Write(self, request: database.WriteRequest, context):
        # Write to all Redis databases
        for client in self.redis_clients:
            client.set(request.title, request.stockValue)
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