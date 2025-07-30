from datetime import datetime

from fastapi import FastAPI

from fianchetto_tradebot.common_models.api.orders.cancel_order_request import CancelOrderRequest
from fianchetto_tradebot.common_models.api.orders.cancel_order_response import CancelOrderResponse
from fianchetto_tradebot.common_models.api.orders.get_order_request import GetOrderRequest
from fianchetto_tradebot.common_models.api.orders.get_order_response import GetOrderResponse
from fianchetto_tradebot.common_models.api.orders.order_list_request import ListOrdersRequest
from fianchetto_tradebot.common_models.api.orders.order_list_response import ListOrdersResponse
from fianchetto_tradebot.common_models.api.orders.place_order_request import PlaceOrderRequest
from fianchetto_tradebot.common_models.api.orders.place_order_response import PlaceOrderResponse
from fianchetto_tradebot.common_models.api.orders.preview_modify_order_request import PreviewModifyOrderRequest
from fianchetto_tradebot.common_models.api.orders.preview_order_request import PreviewOrderRequest
from fianchetto_tradebot.common_models.api.orders.preview_order_response import PreviewOrderResponse
from fianchetto_tradebot.common_models.brokerage.brokerage import Brokerage
from fianchetto_tradebot.common_models.order.order_status import OrderStatus
from fianchetto_tradebot.server.common.api.orders.etrade.etrade_order_service import ETradeOrderService
from fianchetto_tradebot.server.common.api.orders.order_service import OrderService
from fianchetto_tradebot.server.common.brokerage.etrade.etrade_connector import ETradeConnector
from fianchetto_tradebot.server.common.service.rest_service import RestService, ETRADE_ONLY_BROKERAGE_CONFIG
from fianchetto_tradebot.server.common.service.service_key import ServiceKey
from fianchetto_tradebot.server.quotes.etrade.etrade_quotes_service import ETradeQuotesService
from fianchetto_tradebot.server.quotes.quotes_service import QuotesService

JAN_1_2024 = datetime(2024,1,1).date()
DEFAULT_START_DATE = JAN_1_2024
DEFAULT_COUNT = 100


class OrdersRestService(RestService):
    def __init__(self, credential_config_files: dict[Brokerage, str]=ETRADE_ONLY_BROKERAGE_CONFIG):
        super().__init__(ServiceKey.ORDERS, credential_config_files)

    @property
    def app(self) -> FastAPI:
        return self._app

    @app.setter
    def app(self, app: FastAPI):
        self._app = app

    def _register_endpoints(self):
        super()._register_endpoints()
        self.app.add_api_route(path='/api/v1/{brokerage}/accounts/{account_id}/orders', endpoint=self.list_orders, methods=['GET'], response_model=ListOrdersResponse)
        self.app.add_api_route(path='/api/v1/{brokerage}/accounts/{account_id}/orders/{order_id}', endpoint=self.get_order, methods=['GET'], response_model=GetOrderResponse)
        self.app.add_api_route(path='/api/v1/{brokerage}/accounts/{account_id}/orders/preview', endpoint=self.preview_order, methods=['POST'], response_model=PreviewOrderResponse)
        self.app.add_api_route(path='/api/v1/{brokerage}/accounts/{account_id}/orders/preview/{preview_id}', endpoint=self.place_order, methods=['POST'], response_model=PlaceOrderResponse)
        self.app.add_api_route(path='/api/v1/{brokerage}/accounts/{account_id}/orders/preview_and_place', endpoint=self.preview_and_place_order, methods=['POST'], response_model=PlaceOrderResponse)
        self.app.add_api_route(path='/api/v1/{brokerage}/accounts/{account_id}/orders/{order_id}', endpoint=self.cancel_order, methods=['DELETE'], response_model=CancelOrderResponse)
        self.app.add_api_route(path='/api/v1/{brokerage}/accounts/{account_id}/orders/{order_id}', endpoint=self.modify_order, methods=['PUT'], response_model=PlaceOrderResponse)

    def _setup_brokerage_services(self):
        self.order_services: dict[Brokerage, OrderService] = dict()
        self.quotes_services: dict[Brokerage, QuotesService] = dict()

        # E*Trade
        etrade_key: Brokerage = Brokerage.ETRADE
        etrade_connector: ETradeConnector = self.connectors[Brokerage.ETRADE]
        etrade_order_service = ETradeOrderService(etrade_connector)
        etrade_quotes_service = ETradeQuotesService(etrade_connector)

        self.order_services[etrade_key] = etrade_order_service
        self.quotes_services[etrade_key] = etrade_quotes_service

        # TODO: Add for IKBR and Schwab

    def list_orders(self, brokerage: str, account_id: str, status: str = None, from_date: str=None, to_date: str=None, count:int=DEFAULT_COUNT):
        status = OrderStatus.ANY if not status else OrderStatus[status]

        from_date = DEFAULT_START_DATE if not from_date else datetime.datetime.strptime(from_date, '%yyyy-mm-dd').date()
        to_date = datetime.today().date() if not to_date else datetime.datetime.strptime(to_date, '%yyyy-mm-dd').date()

        order_service: OrderService = self.order_services[Brokerage[brokerage.upper()]]
        list_order_request = ListOrdersRequest(account_id=account_id, status=status, from_date=from_date, to_date=to_date, count=count)

        return order_service.list_orders(list_order_request)

    def get_order(self, brokerage: str, account_id: str, order_id: str):
        order_service: OrderService = self.order_services[Brokerage[brokerage.upper()]]
        get_order_request = GetOrderRequest(account_id=account_id, order_id=order_id)

        return order_service.get_order(get_order_request)

    def preview_order(self, brokerage, account_id: str, preview_order_request: PreviewOrderRequest):
        if not preview_order_request.order_metadata.account_id:
            preview_order_request.order_metadata.account_id = account_id

        order_service: OrderService = self.order_services[Brokerage[brokerage.upper()]]
        return order_service.preview_order(preview_order_request)

    def place_order(self, brokerage, account_id: str, preview_id: str, place_order_request: PlaceOrderRequest):
        if not place_order_request.order_metadata.account_id:
            place_order_request.order_metadata.account_id = account_id

        place_order_request.preview_id = preview_id

        order_service: OrderService = self.order_services[Brokerage[brokerage.upper()]]
        return order_service.place_order(place_order_request)

    def preview_and_place_order(self, brokerage, account_id: str, preview_order_request: PreviewOrderRequest):
        if not preview_order_request.order_metadata.account_id:
            preview_order_request.order_metadata.account_id = account_id

        order_service: OrderService = self.order_services[Brokerage[brokerage.upper()]]
        return  order_service.preview_and_place_order(preview_order_request)

    def cancel_order(self, brokerage: str, account_id: str, order_id: str):
        cancel_order_request = CancelOrderRequest(account_id=account_id, order_id=order_id)
        order_service: OrderService = self.order_services[Brokerage[brokerage.upper()]]
        return order_service.cancel_order(cancel_order_request)

    def modify_order(self, brokerage: str, preview_modify_order_request: PreviewModifyOrderRequest):
        order_service: OrderService = self.order_services[Brokerage[brokerage.upper()]]

        return order_service.modify_order(preview_modify_order_request)

    ### Managed Executions - to be cleaved off into a separate service


if __name__ == "__main__":
    oex_app = OrdersRestService()
    oex_app.run(host="0.0.0.0", port=8080)
