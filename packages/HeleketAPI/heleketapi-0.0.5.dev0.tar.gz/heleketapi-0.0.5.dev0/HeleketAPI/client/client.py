from uuid import UUID

from .session.base import BaseSession
from .session._aiohttp import AIOHTTPSession

from HeleketAPI.methods import *
from HeleketAPI.types import *


class HeleketClient:

    def __init__(
        self,
        merchant_id: str,
        api_key: str,
        session: BaseSession | None = None
    ) -> None:
        _session = session or AIOHTTPSession(api_key)
        _session.headers["merchant"] = merchant_id
        self.session = _session

    async def get_payment_info(
        self, uuid: str, order_id: str | None = None
    ) -> PaymentInfoResponse:
        return await self.session(GetPaymentInfo(uuid, order_id))
    
    async def create_invoice(
        self,
        amount: int | float | str,
        currency: str,
        order_id: str,
        *,
        network: str | None = None,
        url_return: str | None = None,
        url_success: str | None = None,
        url_callback: str | None = None,
        is_payment_multiple: bool = True,
        lifetime: int = 3600,
        to_currency: str | None = None,
        subtract: int = 0,
        accuracy_payment_percent: int = 0,
        additional_data: str | None = None,
        currencies: list[str] | None = None,
        except_currencies: list[str] | None = None,
        course_source: str | None = None,
        from_referral_code: str | None = None,
        discount_percent: int | None = None,
        is_refresh: bool = False
    ) -> PaymentInfoResponse:
        if not isinstance(amount, str):
            amount = str(amount)

        return await self.session(
            CreateInvoice(
                amount=amount,
                currency=currency,
                order_id=order_id,
                network=network,
                url_return=url_return,
                url_success=url_success,
                url_callback=url_callback,
                is_payment_multiple=is_payment_multiple,
                lifetime=lifetime,
                to_currency=to_currency,
                subtract=subtract,
                accuracy_payment_percent=accuracy_payment_percent,
                additional_data=additional_data,
                currencies=currencies,
                except_currencies=except_currencies,
                course_source=course_source,
                from_referral_code=from_referral_code,
                discount_percent=discount_percent,
                is_refresh=is_refresh,
            )
        )
    
    async def create_wallet(
        self,
        currency: str,
        network: str,
        order_id: str,
        *,
        url_callback: str | None = None,
        from_referral_code: str | None = None
    ) -> WalletResponse:
        return await self.session(
            CreateWallet(
                currency=currency,
                network=network,
                order_id=order_id,
                url_callback=url_callback,
                from_referral_code=from_referral_code
            )
        )
    
    async def block_wallet(
        self, uuid: str, order_id: str, is_force_refund: bool = False
    ) -> BlockWalletResponse:
        return await self.session(
            BlockWallet(uuid=uuid, order_id=order_id, is_force_refund=is_force_refund)
        )
    
    async def generate_qr(self, uuid: str) -> QRCodeResponse:
        return await self.session(GenerateQRMerchant(uuid))
    
    async def test_webhook_payment(
        self,
        url_callback: str,
        currency: str,
        network: str,
        status: str | None = None,
        uuid: str | UUID | None = None,
        order_id: str | None = None
    ) -> TestWebhookResponse:
        return await self.session(
            TestWebhookPayment(
                url_callback=url_callback,
                currency=currency,
                network=network,
                status=status,
                uuid=uuid,
                order_id=order_id
            )
        )
    
    # async def blocked_address_refund(
    #     self, address: str, *, uuid: str | None = None, order_id: str | None = None
    # ) -> RefundBlockedResponse:
    #     return await self.session(
    #         RefundBlockedResponse(address=address, uuid=uuid, order_id=order_id)
    #     )
    
    # async def refund(
    #     self, address: str, is_subtract: bool, uuid: str | None = None, order_id: str | None = None
    # ) -> RefundResponse:
    #     return await self.session(Refund(address, is_subtract, uuid, order_id))