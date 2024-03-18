import sys
import os
import logging
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from flask import Flask, request
from flask_cors import CORS

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(1, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(2, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import grpc

class Orchestrator:
    def __init__(self):
        channel = grpc.insecure_channel('fraud_detection:50051')
        self.fraud_detection_service = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        channel = grpc.insecure_channel('transaction_verification:50052')
        self.transaction_verification_service = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        channel = grpc.insecure_channel('suggestions:50053')
        self.suggestions_service = suggestions_grpc.SuggestionsServiceStub(channel)


    def initialize_services(self, data, orderId):

        with ThreadPoolExecutor(max_workers=3) as executor:
            order_data = self.get_transaction_verification_order_data(orderId, data)
            executor.submit(self.transaction_verification_service.InitializeOrder, order_data)
            
            order_data = self.get_fraud_detection_order_data(orderId, data)
            executor.submit(self.fraud_detection_service.InitializeOrder, order_data)
            
            order_data = self.get_suggestions_service_order_data(orderId, data)
            executor.submit(self.suggestions_service.InitializeOrder, order_data)


    def process_order(self, order_data):
        # This doesn't guarantee total uniqueness, but I think it's good enough for this example.
        orderId = str(int(time.time())) + str(random.randint(100, 999))
        # Initialize the services with the order data
        self.initialize_services(order_data, orderId)
        request_data = transaction_verification.RequestData(
            orderId=orderId,
            vectorClock=[0, 0, 0]
        )
        verification_response = self.transaction_verification_service.VerifyTransaction(request_data)
        return verification_response


    def get_transaction_verification_order_data(self, orderId, data):
        verification_request = transaction_verification.InitializationRequest(
            orderId=orderId,
            userName=data['user']['name'],
            userContact=data['user']['contact'],
            discountCode=data.get('discountCode', '')
        )

        verification_request.billingAddress.CopyFrom(
            transaction_verification.BillingAddressInfo(**data['billingAddress'])
        )

        verification_request.creditCard.CopyFrom(
            transaction_verification.CreditCardInfo(**data['creditCard'])
        )

        for item in data['items']:
            transaction_item = transaction_verification.TransactionItem(
                name=item['name'],
                quantity=item['quantity']
            )
            verification_request.items.append(transaction_item)

        return verification_request


    def get_fraud_detection_order_data(self, orderId, data):
        fraud_detection_request = fraud_detection.InitializationRequest(
            orderId=orderId,
            creditCardNumber=data['creditCard']['number'],
            creditCardExpirationDate=data['creditCard']['expirationDate'],
            creditCardCVV=data['creditCard']['cvv'],
            discountCode=data['discountCode']
        )

        return fraud_detection_request
    
    def get_suggestions_service_order_data(self, orderId, data):
        item_categories = [item['category'] for item in data['items']]
        suggestions_request = suggestions.InitializationRequest(
            orderId=orderId
        )
        for item in data['items']:
            transaction_item = suggestions.TransactionItem(
                name=item['name']
            )
            suggestions_request.items.extend([transaction_item])
        return suggestions_request


app = Flask(__name__)
CORS(app)

def greet(name='you'):
    return 'Hello, ' + name

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = greet(name='orchestrator')
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Print request object data
    data = request.json
    
    print("Request Data:", data)
    print('Checkout called:', data)

    # Create an instance of the Orchestrator class
    orchestrator = Orchestrator()

    # Process the order
    orchestrator.process_order(data)

"""    with ThreadPoolExecutor(max_workers=3) as executor:
        future_transaction = executor.submit(verify_transaction, data)
        future_fraud = executor.submit(detect_fraud, data)
        future_suggestions = executor.submit(suggest_books, data)
        
        is_transaction_valid = future_transaction.result()
        if not is_transaction_valid:
            print('Invalid transaction')
            return {
                'orderId': '12345',
                'status': 'Order Declined'
            }, 200  # HTTP status code for client error

        fraud_detection_info = future_fraud.result()
        if fraud_detection_info.isFraud:
            print('Fraud detected')
            return {
                'orderId': '12345',
                'status': fraud_detection_info.message
            }, 200
        
        suggested_books = future_suggestions.result()
    
    print('Checkout successful')
    return {
        'orderId': '12345',
        'status': 'Order Approved',
        'suggestedBooks': suggested_books
    }, 200  # HTTP status code for OK"""

if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
