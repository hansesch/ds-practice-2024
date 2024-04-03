import grpc
import sys
import os
import time
import uuid
from google.protobuf.empty_pb2 import Empty
import socket
from concurrent import futures

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(1, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/coordinator'))
sys.path.insert(2, utils_path)

import orderexecutor_pb2 as orderexecutor
import orderexecutor_pb2_grpc as orderexecutor_grpc
import orderqueue_pb2 as orderqueue
import orderqueue_pb2_grpc as orderqueue_grpc
import coordinator_pb2 as coordinator
import coordinator_pb2_grpc as coordinator_grpc

class OrderExecutorService(orderexecutor_grpc.OrderExecutorServiceServicer):
  def __init__(self):
    self.id = str(uuid.uuid4())
    self.connect_to_coordinator()
    self.connect_to_queue()
    self.check_and_execute_order()

  def connect_to_queue(self):
    channel = grpc.insecure_channel('orderqueue:50054')
    self.orderqueue_stub = orderqueue_grpc.OrderQueueServiceStub(channel)

  def connect_to_coordinator(self):
    channel = grpc.insecure_channel('coordinator:50056')
    self.coordinator_stub = coordinator_grpc.CoordinatorServiceStub(channel)

  def check_and_execute_order(self):
    while True:
      request_access = self.coordinator_stub.Request(Empty())
      if request_access.isSuccess:
        order: orderqueue.Order = self.orderqueue_stub.Dequeue(Empty())
        self.coordinator_stub.Release(Empty())
        if order.orderId:
          print(f"Order {order.orderId} is being executed by replica with ID {self.id}...")
          time.sleep(5) # To simulate the time taken to execute the order
          print(f"Execution of order {order.orderId} has finished by replica with ID {self.id}...")
        else:
          print(f"{self.id} Executor: No orders in the queue. Waiting for new orders...")
      else:
        print(f"{self.id} Executor: Another replica is currently leader. Waiting for my turn...")
      time.sleep(5)

def wait_for_service(service, port):
  for _ in range(5):
    try:
      with socket.create_connection((service, port), timeout=5):
        return True
    except OSError:
      print(f"Service at {service}:{port} is not available yet. Retrying...")
      time.sleep(5)
  print(f"Service at {service}:{port} did not become available after 5 attempts.")
  return False


def serve():
    orderqueue_is_up = wait_for_service('orderqueue', '50054')
    if not orderqueue_is_up:
      print("Order Queue service is not available. Exiting...")
      sys.exit(1)
    serviceregister_is_up = wait_for_service('coordinator', '50056')
    if not serviceregister_is_up:
      print("Coordinator service is not available. Exiting...")
      sys.exit(1)

    server = grpc.server(futures.ThreadPoolExecutor())
    orderexecutor_grpc.add_OrderExecutorServiceServicer_to_server(OrderExecutorService(), server)
    port = "50055"
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()