from typing import Any

from tradernet_api.const import Command
from tradernet_api.models.command_model import DeleteOrderModel


def delete_order(self: Any, order_id: str) -> Any:
    """
    Delete/cancel order
    https://tradernet.com/tradernet-api/orders-delete

    :param self: binds with API class
    :param order_id: ID of the order that we want to cancel
    :return: Response
    """
    command_name = Command.delete_order.value

    order_param = DeleteOrderModel(order_id=order_id)

    return self._client_v2.send_request(command=command_name, params=order_param)
