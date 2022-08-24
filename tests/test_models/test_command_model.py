import pytest
from faker import Faker
from pydantic import ValidationError

from tradernet_api.const import Expiration, sides
from tradernet_api.models.command_model import SendOrderModel

faker = Faker()


@pytest.mark.parametrize(
    "input_params,output_dict",
    [
        (
            {
                "instr_name": "AAPL",
                "side": "buy",
                "margin": False,
                "qty": 1,
                "market_order": True,
                "expiry": "day",
            },
            {
                "instr_name": "AAPL",
                "qty": 1,
                "limit_price": 0,
                "stop_price": 0,
                "expiration_id": 1,
                "action_id": 1,
                "order_type_id": 1,
            },
        ),
        (
            {
                "instr_name": "AMD",
                "side": "buy",
                "margin": True,
                "qty": 1,
                "limit_price": 100,
                "expiry": "ext",
            },
            {
                "instr_name": "AMD",
                "qty": 1,
                "limit_price": 100,
                "stop_price": 0,
                "expiration_id": 2,
                "action_id": 2,
                "order_type_id": 2,
            },
        ),
        (
            {
                "instr_name": "GOOGL",
                "side": "sell",
                "margin": False,
                "qty": 1,
                "stop_price": 200,
                "expiry": "gtc",
            },
            {
                "instr_name": "GOOGL",
                "qty": 1,
                "limit_price": 0,
                "stop_price": 200,
                "expiration_id": 3,
                "action_id": 3,
                "order_type_id": 3,
            },
        ),
        (
            {
                "instr_name": "BA",
                "side": "sell",
                "margin": True,
                "qty": 1,
                "limit_price": 200,
                "stop_price": 200,
                "expiry": "gtc",
            },
            {
                "instr_name": "BA",
                "qty": 1,
                "limit_price": 200,
                "stop_price": 200,
                "expiration_id": 3,
                "action_id": 4,
                "order_type_id": 4,
            },
        ),
    ],
)
def test_send_order_model(
    input_params: dict[str, int | str | bool], output_dict: dict[str, int | str]
) -> None:
    """
    Test when all parameters are correct and model return valid dictionary
    :param input_params: parameters that fall into the model
    :param output_dict: expected dict when the method .dict is called
    """
    model = SendOrderModel(**input_params)
    assert model.dict() == output_dict


@pytest.mark.parametrize(
    "input_arg,exception",
    [
        ({"side": faker.word()}, ValidationError),
        ({"limit_price": 0}, ValidationError),
        ({"expiry": faker.word()}, ValidationError),
        ({"side": None}, AttributeError),
        ({"margin": None}, ValidationError),
    ],
)
def test_send_order_model_with_wrong_argument(
    input_arg: dict[str, str | int | None], exception: type[Exception]
) -> None:
    """
    Test when one of input parameter are not correct and model raise error
    :param input_arg: parameter with incorrect value
    :param exception: expected exception
    """
    params = {
        "instr_name": faker.word(),
        "side": faker.word(ext_word_list=sides.keys()),
        "margin": faker.boolean(),
        "qty": faker.unique.random_int(),
        "limit_price": faker.unique.random_int(),
        "expiry": faker.word(ext_word_list=[exp.value for exp in Expiration]),
    }
    params.update(input_arg)
    with pytest.raises(exception):
        SendOrderModel(**params)
