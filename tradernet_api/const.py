from enum import Enum

api_url = "https://tradernet.ru/api"


class Command(Enum):
    send_order = "send_order"
    delete_order = "delete_order"
    get_orders = "get_orders"
    get_ticker_info = "get_ticker_info"
    set_stop_order = "set_stop_order"


class SendOrderField(Enum):
    action_id = "action_id"
    expiry = "expiry"
    expiration_id = "expiration_id"
    side = "side"
    margin = "margin"
    order_type_id = "order_type_id"
    market_order = "market_order"
    limit_price = "limit_price"
    stop_price = "stop_price"


class Order(Enum):
    market = "market"
    limit = "limit"
    stop = "stop"
    stop_limit = "stop_limit"


class Expiration(Enum):
    day = "day"
    ext = "ext"
    gtc = "gtc"


class ModelField(Enum):
    hidden = "hidden"
    exclude = "exclude"


class Errors(Enum):
    side_validation = "side_validation"
    margin_validation = "margin_validation"
    expiration_validation = "expiration_validation"
    order_type_validation = "order_type_validation"


sides = {"buy": 1, "sell": 3}

expirations = {Expiration.day.name: 1, Expiration.ext.name: 2, Expiration.gtc.name: 3}


# Exception messages
EXCEPTION_MESSAGES = {
    Errors.side_validation.name: "Side must be one of: `buy` or `sell`",
    Errors.margin_validation.name: "Margin must be `True` or `False`",
    Errors.expiration_validation.name: f"Expiration must be one of: `{Expiration.day.name}`, "
    f"`{Expiration.ext.name}` or `{Expiration.gtc.name}`",
    Errors.order_type_validation.name: f"One of the order types must be selected: {SendOrderField.market_order.name}, "
    f"{SendOrderField.limit_price.name} or {SendOrderField.stop_price.name}",
}
