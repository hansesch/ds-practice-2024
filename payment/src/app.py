import sys
import os
import time
import logging

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(1, utils_path)
import vector_clock_utils as vector_clock_utils
import payment_pb2 as payment
import payment_pb2_grpc as payment_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudDetectionServiceServicer
class PaymentService(payment_grpc.PaymentServiceServicer):
    order_statuses = dict()

    def PrepareRequest(self, request: payment.PrepareRequest, context):
        if request.orderId in self.order_statuses:
            print(f"Order {request.orderId} cannot be prepared because it is already in state {self.order_statuses[request.orderId]}")
            return payment.PrepareResponse(isReady=False)
        
        self.order_statuses[request.orderId] = 'ready'
        return payment.PrepareResponse(isReady=True)
        
    def CommitRequest(self, request: payment.CommitRequest, context):
        if request.orderId not in self.order_statuses:
            print(f"Order {request.orderId} cannot be commited because it has not been prepared")
            return payment.CommitResponse(isSuccess=False)
        elif self.order_statuses[request.orderId] == 'completed':
            print(f"Order {request.orderId} cannot be commited because it has already been completed")
            return payment.CommitResponse(isSuccess=False)
        else:
            print(f"Payment of order {request.orderId} in progress...")
            time.sleep(1)
            self.order_statuses[request.orderId] = 'completed'
            return payment.CommitResponse(isSuccess=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    payment_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
    port = "50058"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Fraud detection service server started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()