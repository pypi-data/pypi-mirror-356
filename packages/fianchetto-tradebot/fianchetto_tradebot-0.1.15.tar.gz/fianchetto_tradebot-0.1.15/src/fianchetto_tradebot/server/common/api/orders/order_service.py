from fianchetto_tradebot.server.common.api.api_service import ApiService
from fianchetto_tradebot.common_models.api.orders.cancel_order_request import CancelOrderRequest
from fianchetto_tradebot.common_models.api.orders.cancel_order_response import CancelOrderResponse
from fianchetto_tradebot.common_models.api.orders.get_order_request import GetOrderRequest
from fianchetto_tradebot.common_models.api.orders.get_order_response import GetOrderResponse
from fianchetto_tradebot.common_models.api.orders.order_list_request import ListOrdersRequest
from fianchetto_tradebot.common_models.api.orders.order_list_response import ListOrdersResponse
from fianchetto_tradebot.common_models.api.orders.place_modify_order_request import PlaceModifyOrderRequest
from fianchetto_tradebot.common_models.api.orders.place_modify_order_response import PlaceModifyOrderResponse
from fianchetto_tradebot.common_models.api.orders.place_order_request import PlaceOrderRequest
from fianchetto_tradebot.common_models.api.orders.place_order_response import PlaceOrderResponse
from fianchetto_tradebot.common_models.api.orders.preview_modify_order_request import PreviewModifyOrderRequest
from fianchetto_tradebot.common_models.api.orders.preview_modify_order_response import PreviewModifyOrderResponse
from fianchetto_tradebot.common_models.api.orders.preview_order_request import PreviewOrderRequest
from fianchetto_tradebot.common_models.api.orders.preview_order_response import PreviewOrderResponse
from fianchetto_tradebot.server.common.brokerage.connector import Connector


class OrderService(ApiService):
    def __init__(self, connector: Connector):
        super().__init__(connector)

    def list_orders(self, list_orders_request: ListOrdersRequest, brokerage_specific_opts: dict[str, str]=None) -> ListOrdersResponse:
        pass

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        pass

    def cancel_order(self, cancel_order_request: CancelOrderRequest) -> CancelOrderResponse:
        pass

    def preview_modify_order(self, modify_order_request: PreviewModifyOrderRequest) -> PreviewModifyOrderResponse:
        pass

    def place_modify_order(self, modify_order_request: PlaceModifyOrderRequest) -> PlaceModifyOrderResponse:
        pass

    def preview_order(self, preview_order_request: PreviewOrderRequest) -> PreviewOrderResponse:
        pass

    def place_order(self, place_order_request: PlaceOrderRequest) -> PlaceOrderResponse:
        pass

    def preview_and_place_order(self, preview_order_request: PreviewOrderRequest) -> PlaceOrderResponse:
        pass

    def modify_order(self, preview_modify_order_request: PreviewModifyOrderRequest) -> PlaceOrderResponse:
        pass