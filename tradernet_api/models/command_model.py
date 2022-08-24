from typing import Optional

from pydantic import BaseModel, Field, validator

from tradernet_api.const import (
    EXCEPTION_MESSAGES,
    Errors,
    ModelField,
    Order,
    SendOrderField,
    expirations,
    sides,
)


class SendOrderModel(BaseModel):
    instr_name: str
    side: str = Field(hidden=True)
    margin: bool = Field(hidden=True)
    qty: int
    expiry: str = Field(hidden=True)
    market_order: bool = Field(False, hidden=True)
    limit_price: float = 0
    stop_price: float = 0
    expiration_id: Optional[int] = None
    action_id: Optional[int] = None
    order_type_id: Optional[int] = None

    def dict(self, **kwargs):
        hidden_fields = {
            attribute_name
            for attribute_name, model_field in self.__fields__.items()
            if model_field.field_info.extra.get(ModelField.hidden.name) is True
        }
        kwargs.setdefault(ModelField.exclude.name, hidden_fields)
        return super().dict(**kwargs)

    @validator(SendOrderField.action_id.name, always=True)
    def apply_action_id(cls, v, values) -> int:  # type: ignore
        """
        Custom validator for action_id field. Check and convert the input parameters to action_id field by condition.
        :param v: input parameter (default=None)
        :param values: all parameters (default=dict)
        :raises ValueError: if one of the fields (side or margin) has an incorrect value
        :return: integer of action id
        """
        if (
            action_side := sides.get(values.get(SendOrderField.side.name).lower())
        ) is None:
            raise ValueError(EXCEPTION_MESSAGES[Errors.side_validation.name])
        if (action_margin := values.get(SendOrderField.margin.name)) is None:
            raise ValueError(EXCEPTION_MESSAGES[Errors.margin_validation.name])
        return sum((action_side, action_margin))

    @validator(SendOrderField.order_type_id.name, always=True)
    def apply_order_type_id(cls, v, values) -> int:  # type: ignore
        """
        Custom validator for order_type_id field. Check and convert the input parameters to order_type_id
        field by condition.
        :param v: input parameter (default=None)
        :param values: all parameters (default=dict)
        :raises ValueError: if no parameter is passed (market_order, limit_price or stop_price)
        :return: integer of order type id
        """
        types = {
            Order.limit.name: 2
            if bool(values.get(SendOrderField.limit_price.name))
            else 0,
            Order.stop.name: 3
            if bool(values.get(SendOrderField.stop_price.name))
            else 0,
            Order.stop_limit.name: 4
            if (
                bool(values.get(SendOrderField.stop_price.name))
                and bool(values.get(SendOrderField.limit_price.name))
            )
            else 0,
        }
        if values.get(SendOrderField.market_order.name):
            return 1
        elif type_id := max(types.values()):
            return type_id
        raise ValueError(EXCEPTION_MESSAGES[Errors.order_type_validation.name])

    @validator(SendOrderField.expiration_id.name, always=True)
    def apply_expiration_id(cls, v, values) -> int:  # type: ignore
        """
        Custom validator for expiration_id field. Check and convert the input parameters to expiration_id
        field by condition.
        :param v: input parameter (default=None)
        :param values: all parameters (default=dict)
        :raises ValueError: if an invalid value is passed for the expiry field
        :return: integer of expiration id
        """
        if (
            time_exp := expirations.get(values.get(SendOrderField.expiry.name).lower())
        ) is None:
            raise ValueError(EXCEPTION_MESSAGES[Errors.expiration_validation.name])
        return time_exp


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
