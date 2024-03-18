import sys
import os
import logging

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import vector_clock_utils as vector_clock_utils
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudDetectionServiceServicer
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
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
        return fraud_detection.ResponseData(True)

    def DetectFraud(self, request, context):
        print('Detecting fraud:', request)

        response = fraud_detection.FraudDetectionResponse()

        if request.discountCode in self.valid_discount_codes:
            response.isFraud = False
            print('Passed fraud detection.')
        else:
            response.isFraud = True
            response.message = 'Invalid discount code'
            print(response.message)

        # Call the suggestions service.
        suggestions_response = self.call_suggestions_service(request, request_data.vectorClock)
        return suggestions_response
    

    def call_suggestions_service(self, request, vectorClock):
        # Establish a connection with the suggestions gRPC service.
        with grpc.insecure_channel('suggestions:50053') as channel:
            # Create a stub object.
            stub = suggestions_grpc.SuggestionsServiceStub(channel)
            # Create a SuggestionsRequest object.
            suggestions_request = suggestions.SuggestionsRequest(
                orderId=request.orderId,
                vectorClock=vectorClock
            )
            # Call the service through the stub object.
            response = stub.GenerateSuggestions(suggestions_request)
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