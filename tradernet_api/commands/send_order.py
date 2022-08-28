from typing import Any

from tradernet_api.const import Command
from tradernet_api.models.command_model import SendOrderModel


def send_order(
    self: Any,
    ticker: str,
    side: str,
    margin: bool,
    count: int,
    order_exp: str | None = "day",
    market_order: bool | None = False,
    limit_price: float | None = 0,
    stop_price: float | None = 0,
) -> Any:
    """
    A method that allows you to work with the submission of orders for execution.
    https://tradernet.com/tradernet-api/orders-send

    :param self: binds with API class
    :param ticker: Ticker name for execution
    :param side: Action: buy or sell
    :param margin: Use margin or not. Buy with margin or sell with margin
    :param count: Order quantity
    :param order_exp: `day` - order until the of the current trading session,
                      `ext` - day + external hours (pre-market or after hours),
                      `gtc` - good-til-cancelled, until the order is completed or canceled
    :param market_order: Execute market order (optional)
    :param limit_price: Price for limit order (optional)
    :param stop_price: Price for stop order (optional)

    :return: Response
    """
    command_name = Command.send_order.value

    order_param = SendOrderModel(
        instr_name=f"{ticker}.US".upper(),
        side=side,
        margin=margin,
        qty=count,
        expiry=order_exp,
        market_order=market_order,
        limit_price=limit_price,
        stop_price=stop_price,
    )

    return self._client_v2.send_request(command=command_name, params=order_param)
