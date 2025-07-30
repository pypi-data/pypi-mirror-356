from pydantic import BaseModel

from fianchetto_tradebot.common_models.finance.amount import Amount
from fianchetto_tradebot.common_models.order.order import Order


class OrderPreview(BaseModel):
    preview_id: str
    order: Order
    total_order_value: Amount
    estimated_commission: Amount

    def as_preview_id_to_order(self)->(str, Order):
        return self.preview_id, self.order