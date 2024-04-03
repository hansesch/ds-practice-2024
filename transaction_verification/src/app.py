import sys
import os
import re
from datetime import datetime, timedelta
import logging

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/common'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(1, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(2, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/vector_clock'))
sys.path.insert(3, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(4, utils_path)
import common_pb2 as common
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import fraud_detection_pb2_grpc as fraud_detection_grpc
import suggestions_pb2 as suggestions
import vector_clock_utils as vector_clock_utils

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class TransactionVerificationService(transaction_verification_grpc.TransactionVerificationServiceServicer):
    orders = {}
    process_number = 0

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
        print('Transaction Verification: Initialized Order, orderId: ' + request.orderId + ' orderInfo: ' + str(order_info))

        return common.ResponseData(isSuccess=True)
    
    def VerifyCreditCardNumber(self, request: common.RequestData, context):
        print('Transaction Verification: Verifying Credit Card Number, orderId: ' + request.orderId + ' vectorClock: ' + str(self.orders[request.orderId]['vector_clock']))
        order_id = request.orderId
        if order_id in self.orders:
            order_info = self.orders[order_id]
            order_info['vector_clock'] = vector_clock_utils.update_vector_clock(order_info['vector_clock'], 
                                                                                request.vectorClock, 
                                                                                1)
            
            credit_card_number = order_info['order_data']['credit_card_info'].number
            is_valid = re.fullmatch(r'\d{16}', credit_card_number) is not None
            if is_valid:
                print('Credit card number ' + credit_card_number + ' is valid')
                return self.VerifyCreditCardExpiryDate(common.RequestData(orderId=order_id, vectorClock=order_info['vector_clock']), context)
            else:
                print('Credit card number ' + credit_card_number + ' is not valid!')
                return suggestions.SuggestionsResponse(isSuccess=False, items=[], message='Credit card number is not valid!')
        else:
            error_message = 'order with id ' + order_id + ' has not been initialized!'
            print(error_message)
            return suggestions.SuggestionsResponse(isSuccess=False, items=[], message=error_message)
    
    def VerifyCreditCardExpiryDate(self, request: common.RequestData, context):
        print('Transaction Verification: Verifying Credit Card Expiry Date, orderId: ' + request.orderId + ' vectorClock: ' + str(self.orders[request.orderId]['vector_clock']))

        order_id = request.orderId
        if order_id in self.orders:
            order_info = self.orders[order_id]
            order_info['vector_clock'] = vector_clock_utils.update_vector_clock(order_info['vector_clock'], request.vectorClock, 1)
            
            expiration_date = order_info['order_data']['credit_card_info'].expirationDate
            is_valid = False
            try:
                exp_date = datetime.strptime(expiration_date, "%m/%y")
                last_day_of_exp_month = exp_date.replace(day=28) + timedelta(days=4)
                last_day_of_exp_month -= timedelta(days=last_day_of_exp_month.day)
                is_valid = last_day_of_exp_month > datetime.now()
            except ValueError:
                is_valid = False
            if is_valid:
                return self.VerifyOrderItems(common.RequestData(orderId=order_id, vectorClock=order_info['vector_clock']), context)
            else:
                return suggestions.SuggestionsResponse(isSuccess=False, items=[], message="Credit card is expired!")
        else:
            error_message = 'order with id ' + order_id + ' has not been initialized!'
            print(error_message)
            return suggestions.SuggestionsResponse(isSuccess=False, items=[], message=error_message)
        
    def VerifyOrderItems(self, request: common.RequestData, context):
        print('Transaction Verification: Verifying order items, orderId: ' + request.orderId + ' vectorClock: ' + str(self.orders[request.orderId]['vector_clock']))

        order_id = request.orderId
        if order_id in self.orders:
            order_info = self.orders[order_id]
            order_info['vector_clock'] = vector_clock_utils.update_vector_clock(order_info['vector_clock'], request.vectorClock, 1)

            is_valid = True
            order_items = order_info['order_data']['items']
            if not order_items:
                is_valid = False
            for item in order_items:
                if item.quantity <= 0:
                    is_valid = False
            
            if is_valid:
                # Call the fraud-detection service.
                fraud_detection_response = self.call_fraud_detection_service(common.RequestData(orderId=order_id, vectorClock=order_info['vector_clock']))
                print("received response from fraud detection service")
                return fraud_detection_response
            else:
                return suggestions.SuggestionsResponse(isSuccess=False, items=[], message="Order items are not valid!")
        else:
            error_message = 'order with id ' + order_id + ' has not been initialized!'
            print(error_message)
            return suggestions.SuggestionsResponse(isSuccess=False, items=[], message=error_message)
        
    def call_fraud_detection_service(self, request_data: common.RequestData):
        with grpc.insecure_channel('fraud_detection:50051') as channel:
            # Create a stub object.
            stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
            # Call the service through the stub object.
            return stub.DetectFraud(request_data)

    

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