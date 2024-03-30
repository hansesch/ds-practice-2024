import grpc
from concurrent import futures
import sys
import os

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/coordinator'))
sys.path.insert(0, utils_path)

import coordinator_pb2 as coordinator
import coordinator_pb2_grpc as coordinator_grpc

class CoordinatorService(coordinator_grpc.CoordinatorServiceServicer):
    def __init__(self):
        self.isLock = False

    def Request(self, request, context):
        print("Access requested.")
        if self.isLock:
            print("Access denied.")
            return coordinator.Message(isSuccess=False)
        else:
            print("Access granted.")
            self.isLock = True
            return coordinator.Message(isSuccess=True)

    def Release(self, request, context):
        print("Release requested.")
        if self.isLock:
            self.isLock = False
            return coordinator.Message(isSuccess=True)
        else:
            return coordinator.Message(isSuccess=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    coordinator_grpc.add_CoordinatorServiceServicer_to_server(CoordinatorService(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()