from typing import Any

from tradernet_api.models.command_model import GetTickerInfoModel


def get_ticker_info(self: Any, ticker: str, sup: bool | None = False) -> Any:
    """
    Retrieving ticker data from the server.
    https://tradernet.com/tradernet-api/quotes-get-info

    :param self: binds with API class
    :param ticker: the name of the ticker, required to retrieve data from the server
    :param sup: IMS and trading system format. Optional
    :return: Response (https://tradernet.com/tradernet-api/securities)
    """
    command_name = "getSecurityInfo"

    order_param = GetTickerInfoModel(ticker=f"{ticker}.US".upper(), sup=sup)

    return self._client_v1.send_request(command=command_name, params=order_param)
