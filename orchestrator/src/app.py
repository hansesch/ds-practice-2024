import sys
import os
import logging
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from flask import Flask, request
from flask_cors import CORS
from google.protobuf.json_format import MessageToDict

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

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
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(3, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(4, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(5, utils_path)
import common_pb2 as common
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import orderqueue_pb2 as orderqueue
import orderqueue_pb2_grpc as orderqueue_grpc
import orderexecutor_pb2 as orderexecutor
import orderexecutor_pb2_grpc as orderexecutor_grpc
import grpc
from google.protobuf.empty_pb2 import Empty


resource = Resource(attributes={
    SERVICE_NAME: "orderqueue"
})
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics")
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)
meter = meterProvider.get_meter(name="Orchestrator")

class Orchestrator:
    def __init__(self):
        channel = grpc.insecure_channel('fraud_detection:50051')
        self.fraud_detection_service = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        channel = grpc.insecure_channel('transaction_verification:50052')
        self.transaction_verification_service = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        channel = grpc.insecure_channel('suggestions:50053')
        self.suggestions_service = suggestions_grpc.SuggestionsServiceStub(channel)
        self.order_counter = meter.create_counter(name="OrchestratorOrdersProcessedCounter")


    def initialize_services(self, data, orderId):
        with ThreadPoolExecutor(max_workers=3) as executor:
            order_data = self.get_transaction_verification_order_data(orderId, data)
            executor.submit(self.transaction_verification_service.InitializeOrder, order_data)
            
            order_data = self.get_fraud_detection_order_data(orderId, data)
            executor.submit(self.fraud_detection_service.InitializeOrder, order_data)
            
            order_data = self.get_suggestions_service_order_data(orderId, data)
            executor.submit(self.suggestions_service.InitializeOrder, order_data)


    def process_order(self, order_id, order_data):
        # Initialize the services with the order data
        self.initialize_services(order_data, order_id)
        request_data = common.RequestData(
            orderId=order_id,
            vectorClock=[0, 0, 0]
        )
        response = self.transaction_verification_service.VerifyCreditCardNumber(request_data)
        self.order_counter.add(1)
        return response


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
        suggestions_request = suggestions.InitializationRequest(
            orderId=orderId
        )
        for item in data['items']:
            transaction_item = suggestions.TransactionItem(
                name=item['category']
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
    


    # Create an instance of the Orchestrator class
    orchestrator = Orchestrator()

    # This doesn't guarantee total uniqueness, but I think it's good enough for this example.
    order_id = str(int(time.time())) + str(random.randint(100, 999))

    print('Checkout called, assigning OrderID:', order_id)
    # Process the order
    final_suggestion_response: suggestions.SuggestionsResponse = orchestrator.process_order(order_id, data)

    if not final_suggestion_response.isSuccess:
        print('OrderId: ' + order_id + ' Invalid transaction: ' + final_suggestion_response.message)
        return {
            'orderId': order_id,
            'status': final_suggestion_response.message
        }, 200  
    else:
        suggested_books = [MessageToDict(item) for item in final_suggestion_response.items]

        #print('Transaction is valid, received suggested books:')
        #print(suggested_books)
        print('Putting order ' + order_id + ' into order queue')
        with grpc.insecure_channel('orderqueue:50054') as channel:  
            stub = orderqueue_grpc.OrderQueueServiceStub(channel)
            total_items = sum([item['quantity'] for item in data['items']])
            order_items = [orderqueue.OrderItem(id=item['id'], quantity=item['quantity']) for item in data['items']]

            confirmation: orderqueue.Confirmation = stub.Enqueue(orderqueue.Order(orderId=order_id, items=order_items, orderQuantity=total_items))
        if confirmation.isSuccess:
            print('Received confirmation from order queue about order enqueueing for OrderID:', order_id)
            return {
                'orderId': order_id,
                'status': 'Order Approved',
                'suggestedBooks': suggested_books
            }, 200
        else:
            print('order queue failed to enqueue order, OrderID:', order_id)
            return {
            'orderId': order_id,
            'status': 'Failed to enqueue order'
            }, 500  


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0', debug=True)
