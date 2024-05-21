import grpc
from concurrent import futures
import sys
import os
import threading 

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/coordinator'))
sys.path.insert(0, utils_path)

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
meter = meterProvider.get_meter(name="Coordinator")

class CoordinatorService(coordinator_grpc.CoordinatorServiceServicer):
    def __init__(self):
        self.isLock = False
        self.lock_timer = None
        self.lock_gauge = meter.create_observable_gauge(name="CoordinatorLockGauge", callbacks=self.gauge_lock)

    def gauge_lock(self):
        return self.isLock

    def Request(self, request, context):
        #print("Access requested.")
        if self.isLock:
            #print("Access denied.")
            return coordinator.Message(isSuccess=False)
        else:
            self.isLock = True
            self.lock_timer = threading.Timer(60.0, self.auto_release)
            self.lock_timer.start()
            #print("Access granted.")
            return coordinator.Message(isSuccess=True)

    def Release(self, request, context):
        #print("Release requested.")
        if self.isLock:
            self.isLock = False
            if self.lock_timer is not None:
                self.lock_timer.cancel()
            #print('Release granted.')
            return coordinator.Message(isSuccess=True)
        else:
            #print('Release denied - nothing to release')
            return coordinator.Message(isSuccess=False)

    def auto_release(self):
        #print("Auto releasing the lock.")
        self.isLock = False

        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    coordinator_grpc.add_CoordinatorServiceServicer_to_server(CoordinatorService(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()