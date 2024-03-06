import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

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
import logging

def greet(name='you'):
    return 'Hello, ' + name

def detect_fraud(data):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        fraud_detection_request = fraud_detection.FraudDetectionRequest(
            creditCardNumber=data['creditCard']['number'],
            creditCardExpirationDate=data['creditCard']['expirationDate'],
            creditCardCVV=data['creditCard']['cvv'],
            discountCode=data['discountCode']
        )
        # Call the service through the stub object.
        response = stub.DetectFraud(fraud_detection_request)
    return response

def suggest_books(data):
    item_categories = [item['category'] for item in data['items']]

    # Establish a connection with the suggestions gRPC service.
    with grpc.insecure_channel('suggestions:50053') as channel:
        # Create a stub object.
        stub = suggestions_grpc.SuggestionsServiceStub(channel)
        # Create the request object.
        request = suggestions.SuggestionsRequest()
        request.items.extend(item_categories) 
        
        # Call the service through the stub object.
        response = stub.SuggestItems(request)

    suggested_books = [{
        'bookId': item.bookId,
        'title': item.title,
        'author': item.author
    } for item in response.items]

    return suggested_books

def verify_transaction(data):
    # Establish a connection with the transaction-verification gRPC service.
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        # Create a stub object.
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)

        verification_request = transaction_verification.VerificationRequest(
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

        # Call the service through the stub object.
        response = stub.VerifyTransaction(verification_request)
    return response.isValid

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)

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

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_transaction = executor.submit(verify_transaction, data)
        future_fraud = executor.submit(detect_fraud, data)
        future_suggestions = executor.submit(suggest_books, data)
        
        is_transaction_valid = future_transaction.result()
        
        if not is_transaction_valid: 
            print('Invalid transaction')

        if not is_transaction_valid:
            return {
                'orderId': '12345',
                'status': 'Order Declined'
            }, 200  # HTTP status code for client error
        fraud_detection_info = future_fraud.result()

        if fraud_detection_info.isFraud: 
            print('Fraud detected')

        if fraud_detection_info.isFraud:
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
    }, 200  # HTTP status code for OK


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
