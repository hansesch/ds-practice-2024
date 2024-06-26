import grpc
import sys
import os
import time
import uuid
from google.protobuf.empty_pb2 import Empty
import socket
from concurrent import futures

from opentelemetry import metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderexecutor'))
sys.path.insert(0, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(1, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/coordinator'))
sys.path.insert(2, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(3, utils_path)
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(4, utils_path)

import database_pb2 as database
import database_pb2_grpc as database_grpc
import payment_pb2 as payment
import payment_pb2_grpc as payment_grpc
import orderexecutor_pb2 as orderexecutor
import orderexecutor_pb2_grpc as orderexecutor_grpc
import orderqueue_pb2 as orderqueue
import orderqueue_pb2_grpc as orderqueue_grpc
import coordinator_pb2 as coordinator
import coordinator_pb2_grpc as coordinator_grpc

resource = Resource(attributes={
    SERVICE_NAME: "orderqueue"
})

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics")
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)
meter = meterProvider.get_meter(name="Order Executor")


class OrderExecutorService(orderexecutor_grpc.OrderExecutorServiceServicer):
  def __init__(self):
    self.id = str(uuid.uuid4())
    self.connect_to_coordinator()
    self.connect_to_queue()
    self.order_counter = meter.create_counter(name="OrdersExecutedCounter")
    self.fetch_order()

  def connect_to_queue(self):
    channel = grpc.insecure_channel('orderqueue:50054')
    self.orderqueue_stub = orderqueue_grpc.OrderQueueServiceStub(channel)

  def connect_to_coordinator(self):
    channel = grpc.insecure_channel('coordinator:50056')
    self.coordinator_stub = coordinator_grpc.CoordinatorServiceStub(channel)

  def process_order(self, order):
    for item in order.items:
      with grpc.insecure_channel(f'database:50057') as database_channel:
        with grpc.insecure_channel(f'payment:50058') as payment_channel:
          database_stub = database_grpc.DatabaseServiceStub(database_channel)
          payment_stub = payment_grpc.PaymentServiceStub(payment_channel)
          
          prepareDecrementResponse = database_stub.PrepareDecrementStock(database.PrepareDecrementStockRequest(orderId=order.orderId, id=item.id, decrement=item.quantity))
          preparePaymentResponse = payment_stub.PreparePayment(payment.PrepareRequest(orderId=order.orderId))
          if not prepareDecrementResponse.isReady:
            print(f"Database service is not ready to update stock values")
          elif not preparePaymentResponse.isReady:
            print(f"Payment service is not ready to process payment")
          else:
            commitDecrementResponse = database_stub.CommitDecrementStock(database.CommitRequest(orderId=order.orderId))
            commitPaymentResponse = payment_stub.CommitPayment(payment.CommitRequest(orderId=order.orderId))
            if commitDecrementResponse.isSuccess:
              print(f"Stock of item {item.id} decremented by {item.quantity}.")
            else:
              print(f"Stock of item {item.id} could not be decremented due to failure in committing decrement.")
            if commitPaymentResponse.isSuccess:
              print(f"Processed payment for item {order.orderId}.")
            else:
              print(f"Payment for item {order.orderId} could not be processed due to failure in committing the payment.")
            self.order_counter.add(1)

  def fetch_order(self):
    while True:
      time.sleep(5)
      request_access = self.coordinator_stub.Request(Empty())
      if request_access.isSuccess:
        order: orderqueue.Order = self.orderqueue_stub.Dequeue(Empty())
        self.coordinator_stub.Release(Empty())
        if order.orderId:
          print(f"Order {order.orderId} is being executed by replica with ID {self.id}...")
          self.process_order(order)
          time.sleep(5) # To simulate the time taken to execute the order
          print(f"Execution of order {order.orderId} has finished by replica with ID {self.id}...")
      # removed to reduce spam
      #  else:
      #    print(f"{self.id} Executor: No orders in the queue. Waiting for new orders...")
      #else:
      #  print(f"{self.id} Executor: Another replica is currently leader. Waiting for my turn...")
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