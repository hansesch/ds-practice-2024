import grpc
from concurrent import futures
import sys
import os

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(0, utils_path)

import orderqueue_pb2 as orderqueue
import orderqueue_pb2_grpc as orderqueue_grpc

class OrderQueueService(orderqueue_grpc.OrderQueueServiceServicer):
  def __init__(self):
    self.queue = []

  def Enqueue(self, request, context):
    self.queue.append(request)
    return orderqueue.Confirmation(isSuccess=True, message="Order enqueued")

  def Dequeue(self, request, context):
    if not self.queue:
      context.abort(grpc.StatusCode.NOT_FOUND, "No orders in queue")
    return self.queue.pop(0)
  
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    orderqueue_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
    # Listen on port 50054
    port = "50054"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Order Queue service server started. Listening on port 50054.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()



