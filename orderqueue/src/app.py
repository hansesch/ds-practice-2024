import grpc
from concurrent import futures
import sys
import os
import bisect

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from functools import cmp_to_key
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/orderqueue'))
sys.path.insert(0, utils_path)

import orderqueue_pb2 as orderqueue
import orderqueue_pb2_grpc as orderqueue_grpc

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "orderqueue"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4318/v1/traces"))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)
tracer = trace.get_tracer("orderqueue.tracer")

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics")
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)


class OrderQueueService(orderqueue_grpc.OrderQueueServiceServicer):
  def __init__(self):
    self.queue = []
    self.meter = meterProvider.get_meter(name="Order Queue")
    self.queue_size_counter = self.meter.create_up_down_counter(name="OrderQueueSizeCounter")

  def Enqueue(self, request: orderqueue.Order, context):
    print(f"Order {request.orderId} enqueued")
    bisect.insort(self.queue, (request.orderQuantity, request), key=cmp_to_key(lambda x, y: x[0] - y[0]))
    return orderqueue.Confirmation(isSuccess=True, message="Order enqueued")

  def Dequeue(self, request, context):
    if self.queue:
        with tracer.start_as_current_span("orderqueue.order.dequeued") as span:
          _, order = self.queue.pop(0)
          self.queue_size_counter.add(-1)
          span.set_attribute("order_id", order.orderId)
          print(f"Order {order.orderId} dequeued")
        return order
    else:
        #print("No orders in the queue.")
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



