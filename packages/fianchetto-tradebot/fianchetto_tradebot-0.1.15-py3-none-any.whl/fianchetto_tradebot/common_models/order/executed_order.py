from pydantic import BaseModel

from fianchetto_tradebot.common_models.order.executed_order_details import ExecutionOrderDetails
from fianchetto_tradebot.common_models.order.placed_order import PlacedOrder


class ExecutedOrder(BaseModel):
    order: PlacedOrder
    execution_order_details: ExecutionOrderDetails

    def get_order(self):
        return self.order