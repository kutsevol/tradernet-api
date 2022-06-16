from typing import Optional

from pydantic import BaseModel


class SendOrderModel(BaseModel):
    instr_name: str
    action_id: int
    order_type_id: int
    qty: int
    expiration_id: int
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None


class SetStopOrderModel(BaseModel):
    ticker: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class GetTickerInfoModel(BaseModel):
    ticker: str
    sup: Optional[bool] = None


class GetOrdersModel(BaseModel):
    active_only: Optional[bool] = None


class DeleteOrderModel(BaseModel):
    order_id: int
