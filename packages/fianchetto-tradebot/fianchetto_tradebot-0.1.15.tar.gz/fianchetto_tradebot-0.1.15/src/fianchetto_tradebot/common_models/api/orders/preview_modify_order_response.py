from typing import Optional

from fianchetto_tradebot.common_models.api.orders.preview_order_response import PreviewOrderResponse


class PreviewModifyOrderResponse(PreviewOrderResponse):
    previous_order_id: Optional[str]
