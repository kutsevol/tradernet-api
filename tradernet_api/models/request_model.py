from typing import Union

from pydantic import BaseModel

from tradernet_api.models.command_model import (
    DeleteOrderModel,
    GetOrdersModel,
    GetTickerInfoModel,
    SendOrderModel,
    SetStopOrderModel,
)


class Request(BaseModel):
    cmd: str
    params: Union[
        GetOrdersModel,
        GetTickerInfoModel,
        DeleteOrderModel,
        SendOrderModel,
        SetStopOrderModel,
    ]
    nonce: int

    class Config:
        smart_union = True


class RequestV1(Request):
    sig: str


class RequestV2(Request):
    apiKey: str
