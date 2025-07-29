from dataclasses import dataclass
from uuid import UUID

from .base import Method
from ..types import TestWebhookResponse


@dataclass
class TestWebhookPayment(Method[TestWebhookResponse]):
    __returning__ = TestWebhookResponse
    __api_method__ = "v1/test-webhook/payment"
    __http_method__ = "post"
    
    url_callback: str
    currency: str
    network: str
    status: str
    uuid: str | UUID | None = None
    order_id: str | None = None
    