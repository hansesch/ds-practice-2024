import grpc
from concurrent import futures
import sys
import os
import bisect

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(0, utils_path)

import orderqueue_pb2 as orderqueue
import orderqueue_pb2_grpc as orderqueue_grpc

class OrderQueueService(orderqueue_grpc.OrderQueueServiceServicer):
  def __init__(self):
    self.queue = []

  def Enqueue(self, request, context):
    print(f"Order {request.orderId} enqueued")
    bisect.insort(self.queue, (request.orderQuantity, request))
    return orderqueue.Confirmation(isSuccess=True, message="Order enqueued")

  def Dequeue(self, request, context):
    if self.queue:
        _, order = self.queue.pop(0)
        print(f"Order {order.orderId} dequeued")
        return order
    else:
        print("No orders in the queue.")
        return orderqueue.Order()  # Return an empty Order object

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    orderqueue_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
    port = "50054"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Order Queue service server started. Listening on port 50054.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()



