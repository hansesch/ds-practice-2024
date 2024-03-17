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
    orders = {}

    def InitializeOrder(self, request: transaction_verification.InitializationRequest, context):
        order_info = {
            'vector_clock': [0, 0, 0],
            'order_data': {
                'items': request.items,
                'user_name': request.userName,
                'user_contact': request.userContact,
                'discout_code': request.discountCode,
                'billing_address': request.billingAddress,
                'credit_card_info': request.creditCard
            }
        }
        self.orders[request.orderId] = order_info
        return transaction_verification.ResponseData(True)
    
    def VerifyCreditCardNumber(self, request: transaction_verification.RequestData, context):
        order_id = request.orderId
        if order_id in self.orders:
            credit_card_number = self.orders[order_id]['order_data']['credit_card_info'].number
            is_valid = re.fullmatch(r'\d{16}', credit_card_number) is not None
            return transaction_verification.ResponseData(is_valid)
        else:
            print('order with id ' + order_id + ' has not been initialized!')
            return transaction_verification.ResponseData(False)
    
    def VerifyCreditCardExpiryDate(self, request, context):
        order_id = request.orderId
        is_valid = False
        if order_id in self.orders:
            expiration_date = self.orders[order_id]['order_data']['credit_card_info'].expirationDate
            try:
                exp_date = datetime.strptime(expiration_date, "%m/%y")
                last_day_of_exp_month = exp_date.replace(day=28) + timedelta(days=4)
                last_day_of_exp_month -= timedelta(days=last_day_of_exp_month.day)
                is_valid = last_day_of_exp_month > datetime.now()
            except ValueError:
                is_valid = False
            return transaction_verification.ResponseData(is_valid)
        else:
            print('order with id ' + order_id + ' has not been initialized!')
            return transaction_verification.ResponseData(False)
        
    def VerifyOrderItems(self, request, context):
        order_id = request.orderId
        if order_id in self.orders:
            is_valid = True
            order_items = self.orders[order_id]['order_data']['items']
            if not order_items:
                is_valid = False
            for item in order_items:
                if item.quantity <= 0:
                    is_valid = False
            return transaction_verification.ResponseData(is_valid)
        else:
            print('order with id ' + order_id + ' has not been initialized!')
            return transaction_verification.ResponseData(False)
    

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