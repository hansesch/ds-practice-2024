import sys
import os
import re
from datetime import datetime, timedelta
import logging

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class TransactionVerificationService(transaction_verification_grpc.TransactionVerificationServiceServicer):
    vector_clocks = {}

    def VerifyTransaction(self, request: transaction_verification.VerificationRequest, context):
        print('Verifying transaction:', request)
        def update_vector_clock(order_id, vector_clock):
            if order_id not in self.vector_clocks:
                self.vector_clocks[order_id] = vector_clock
            else:
                existing_clock = self.vector_clocks[order_id]
                existing_clock[0] = max(existing_clock[0], vector_clock[0] + 1)
                self.vector_clocks[order_id] = existing_clock

        def check_credit_card_number(number):
            return re.fullmatch(r'\d{16}', number) is not None
        
        def check_expiry_date(expiration_date):
            try:
                exp_date = datetime.strptime(expiration_date, "%m/%y")
                last_day_of_exp_month = exp_date.replace(day=28) + timedelta(days=4)
                last_day_of_exp_month -= timedelta(days=last_day_of_exp_month.day)
                return last_day_of_exp_month > datetime.now()
            except ValueError:
                return False 

        def check_items(items):
            if not items:
                return False
            for item in items:
                if item.quantity <= 0:
                    return False
            return True
        
        order_id = request.orderId
        update_vector_clock(order_id, request.vectorClock)
        
        response = transaction_verification.VerificationResponse()
        response.orderId = order_id
        response.vectorClock = self.vector_clocks[order_id]
        
        if not check_credit_card_number(request.creditCard.number):
            response.isValid = False
            response.message = "Invalid credit card number"
            print(response.message)
            return response
        elif not check_expiry_date(request.creditCard.expirationDate):
            response.isValid = False
            response.message = "Expiration date invalid"
            print(response.message)
            return response
        elif not check_items(request.items):
            response.isValid = False
            response.message = "Invalid quantity"
            print(response.message)
            return response

        response.isValid = True
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    transaction_verification_grpc.add_TransactionVerificationServiceServicer_to_server(TransactionVerificationService(), server)
    # Listen on port 50052
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Transaction verification service server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()