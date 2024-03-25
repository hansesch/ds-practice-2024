import sys
import os
import logging

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/common'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(1, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(2, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/vector_clock'))
sys.path.insert(3, utils_path)
import vector_clock_utils as vector_clock_utils
import common_pb2 as common;
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudDetectionServiceServicer
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
    process_number = 1
    orders = {}
    valid_discount_codes = ['47289142', '91247892042', '1927301293', '0129701293', '012937201']

    def InitializeOrder(self, request: fraud_detection.InitializationRequest, context):
        order_info = {
            'vector_clock': [0, 0, 0],
            'order_data': {
                'creditCardNumber': request.creditCardNumber,
                'creditCardExpirationDate': request.creditCardExpirationDate,
                'creditCardCVV': request.creditCardCVV,
                'discountCode': request.discountCode
            }
        }
        self.orders[request.orderId] = order_info
        print('Fraud Detection service: Initialized order with id ' + request.orderId + ', order data: ' + str(order_info['order_data']))

        return common.ResponseData(isSuccess=True)

    def DetectFraud(self, request: common.RequestData, context):
        order_id = request.orderId
        print('Fraud Detection: Checking discount codes, orderId: ' + order_id + ' vector clock before operation: ' + str(self.orders[request.orderId]['vector_clock']))

        if order_id in self.orders:
            order_info = self.orders[order_id]

            order_info['vector_clock'] = vector_clock_utils.update_vector_clock(order_info['vector_clock'], 
                                                                                request.vectorClock, 
                                                                                0)
            
            print('updated vector clock: ' + str(order_info['vector_clock']))

            if not order_info['order_data']['discountCode'] or order_info['order_data']['discountCode'] in self.valid_discount_codes:
                print('Passed fraud detection. Calling suggestions service next')

                request_data = common.RequestData(
                    orderId=order_id,
                    vectorClock=order_info['vector_clock']
                )
                suggestions_response = self.call_suggestions_service(request_data)
                print("Received response from Suggestions service")
                return suggestions_response
            else:
                error_message = 'Invalid discount code. Did not pass fraud detetction.'
                print(error_message)
                return suggestions.SuggestionsResponse(isSuccess=False, items=[], message=error_message)
        else:
            error_message = 'order with id ' + order_id + ' has not been initialized!'
            print(error_message)
            return suggestions.SuggestionsResponse(isSuccess=False, items=[], message=error_message)
            
        

    def call_suggestions_service(self, request_data: common.RequestData):
        # Establish a connection with the suggestions gRPC service.
        with grpc.insecure_channel('suggestions:50053') as channel:
            # Create a stub object.
            stub = suggestions_grpc.SuggestionsServiceStub(channel)
            # Call the service through the stub object.
            response = stub.SuggestItems(request_data)
        return response
    

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    fraud_detection_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Fraud detection service server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()