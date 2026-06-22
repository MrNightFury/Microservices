# /app/services/delivery_service.py 

class DeliveryService(): 
    delivery_repo: DeliveryRepo 
    deliveryman_repo: DeliverymenRepo 
 
    def __init__(self) -> None: 
        self.delivery_repo = DeliveryRepo() 
        self.deliveryman_repo = DeliverymenRepo()

    def get_deliveries(self) -> list[Delivery]: 
        return self.delivery_repo.get_deliveries()
    
    def create_delivery(self, order_id: UUID, date: datetime, address: str) -> Delivery: 
        delivery = Delivery(id=order_id, address=address, date=date, status=DeliveryStatuses.CREATED) 
        return self.delivery_repo.create_delivery(delivery)
    
    def activate_delivery(self, id: UUID) -> Delivery: 
        delivery = self.delivery_repo.get_delivery_by_id(id) 
        if delivery.status != DeliveryStatuses.CREATED: 
            raise ValueError 
        delivery.status = DeliveryStatuses.ACTIVATED 
        return self.delivery_repo.set_status(delivery)
     
    def set_deliveryman(self, delivery_id, deliveryman_id) -> Delivery: 
        delivery = self.delivery_repo.get_delivery_by_id(delivery_id) 
        try: 
            deliveryman = self.deliveryman_repo.get_deliveryman_by_id(deliveryman_id) 
        except KeyError: 
            raise ValueError 
        if delivery.status != DeliveryStatuses.ACTIVATED: 
            raise ValueError 
        delivery.deliveryman = deliveryman 
        return self.delivery_repo.set_deliveryman(delivery) 
    
    def finish_delivery(self, id: UUID) -> Delivery: 
        delivery = self.delivery_repo.get_delivery_by_id(id) 
        if delivery.status != DeliveryStatuses.ACTIVATED: 
            raise ValueError 
        delivery.status = DeliveryStatuses.DONE 
        return self.delivery_repo.set_status(delivery) 
    
    def cancel_delivery(self, id: UUID) -> Delivery: 
        delivery = self.delivery_repo.get_delivery_by_id(id) 
        if delivery.status == DeliveryStatuses.DONE: 
            raise ValueError 
        delivery.status = DeliveryStatuses.CANCELED 
        return self.delivery_repo.set_status(delivery) 
    

# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def setup_tracing(service_name: str = "my-service"):
    # 1. Ресурс описывает, кто отправляет телеметрию
    resource = Resource.create({
        "service.name": service_name,
    })

    # 2. Провайдер трейсера
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # 3. Экспорт спанов в Jaeger по OTLP/HTTP
    exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces",
    )
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    return trace.get_tracer(__name__)


# app.py (FastAPI)
from fastapi import FastAPI
from tracing import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Инициализация ДО создания приложения
setup_tracing(service_name="order-service")

app = FastAPI()

# Автоинструментирование FastAPI, HTTP-клиента и SQLAlchemy
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
SQLAlchemyInstrumentor().instrument()

@app.get("/api/orders")
def get_orders():
    # Спан для входящего запроса создан автоматически
    return {"orders": []}

from sqlalchemy.orm import declarative_base