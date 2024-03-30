import grpc
from concurrent import futures
import sys
import os
import threading 

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/coordinator'))
sys.path.insert(0, utils_path)

import coordinator_pb2 as coordinator
import coordinator_pb2_grpc as coordinator_grpc

class CoordinatorService(coordinator_grpc.CoordinatorServiceServicer):
    def __init__(self):
        self.isLock = False
        self.lock_timer = None

    def Request(self, request, context):
        print("Access requested.")
        if self.isLock:
            print("Access denied.")
            return coordinator.Message(isSuccess=False)
        else:
            print("Access granted.")
            self.isLock = True
            self.lock_timer = threading.Timer(60.0, self.auto_release)
            self.lock_timer.start()
            return coordinator.Message(isSuccess=True)

    def Release(self, request, context):
        print("Release requested.")
        if self.isLock:
            self.isLock = False
            if self.lock_timer is not None:
                self.lock_timer.cancel()
            return coordinator.Message(isSuccess=True)
        else:
            return coordinator.Message(isSuccess=False)

    def auto_release(self):
        print("Auto releasing the lock.")
        self.isLock = False

        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    coordinator_grpc.add_CoordinatorServiceServicer_to_server(CoordinatorService(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()