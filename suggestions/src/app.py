import sys
import os
import requests
import logging

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/common'))
sys.path.insert(1, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/vector_clock'))
sys.path.insert(2, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc
import common_pb2 as common
import vector_clock_utils as vector_clock_utils

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# suggestions_pb2_grpc.HelloServiceServicer
class SuggestionsService(suggestions_grpc.SuggestionsServiceServicer):
    orders = {}
    process_number = 2

    def InitializeOrder(self, request: suggestions.InitializationRequest, context):
        order_info = {
            'vector_clock': [0, 0, 0],
            'order_data': {
                'items': request.items
            }
        }
        self.orders[request.orderId] = order_info
        #print('Suggestions service: Initialized order with id ' + request.orderId + ', order data: ' + str(order_info['order_data']))
        print('Initialized order with id ' + request.orderId)

        return common.ResponseData(isSuccess=True)
        
    def SuggestItems(self, request: common.RequestData, context):
        order_id = request.orderId
        print('Suggesting books, orderId: ' + order_id + ' vector clock before operation: ' + str(self.orders[request.orderId]['vector_clock']))

        if order_id in self.orders:
            order_info = self.orders[order_id]

            suggestion_result = get_suggestions(order_info['order_data']['items'])
            #print('Got Suggestions: ', suggestion_result)
            order_info['vector_clock'] = vector_clock_utils.update_vector_clock(order_info['vector_clock'], 
                                                                                request.vectorClock, 
                                                                                2)
            print("OrderId: " + order_id + " Vector clock after operation: " + str(order_info['vector_clock']))
            
            response = suggestions.SuggestionsResponse(isSuccess=True)
            for suggestion in suggestion_result:
                suggested_item = response.items.add()
                suggested_item.bookId = suggestion['bookId']
                suggested_item.title = suggestion['title']
                suggested_item.author = suggestion['author']
            return response
        else:
            error_message = 'order with id ' + order_id + ' has not been initialized!'
            print(error_message)
            return suggestions.SuggestionsResponse(isSuccess=False, items=[], message=error_message)

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    suggestions_grpc.add_SuggestionsServiceServicer_to_server(SuggestionsService(), server)
    # Listen on port 50053
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Suggestions service server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()


def get_suggestions(purchased_items):
    suggestions = []
    category = purchased_items[0].name.replace('_', ' ').lower()
    #print(f"Fetching suggestions for category: {category}")
    url = f"https://openlibrary.org/subjects/{category}.json?limit=3"
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()

        for book in data['works']:
            suggestions.append(
                {
                    "bookId": book['key'].replace('/works/', ''),
                    "title": book['title'],
                    "author": ', '.join(author['name'] for author in book.get('authors', []))
                }
            )
    except requests.RequestException as e:
        print(f"Error fetching data from Open Library: {e}")
    return suggestions

if __name__ == '__main__':
    serve()