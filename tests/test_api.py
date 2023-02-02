import json

from faker import Faker
from requests_mock import Mocker

from tradernet_api.api import API
from tradernet_api.client import ClientV2
from tradernet_api.const import Expiration, api_url, sides

faker = Faker()


def test_send_order_wrong_api_and_secret_keys(test_client: API) -> None:
    response = test_client.send_order(  # type: ignore
        ticker=faker.word(),
        side=faker.word(ext_word_list=sides.keys()),
        margin=faker.boolean(),
        count=faker.unique.random_int(),
        order_exp=faker.word(ext_word_list=[exp.value for exp in Expiration]),
        limit_price=faker.unique.random_int(),
    )

    assert json.loads(response.content.decode())["code"] == 4
    assert (
        "No matching pair is found for apiKey:"
        in json.loads(response.content.decode())["error"]
    )


def test_delete_order_wrong_api_and_secret_keys(test_client: API) -> None:
    response = test_client.delete_order(order_id=faker.unique.random_int())  # type: ignore

    assert json.loads(response.content.decode())["code"] == 4
    assert (
        "No matching pair is found for apiKey:"
        in json.loads(response.content.decode())["error"]
    )


def test_get_orders_wrong_api_and_secret_keys(test_client: API) -> None:
    response = test_client.get_orders(active_only=False)  # type: ignore
    assert json.loads(response.content.decode())["code"] == 4
    assert (
        "No matching pair is found for apiKey:"
        in json.loads(response.content.decode())["error"]
    )


def test_set_stop_order_wrong_api_and_secret_keys(test_client: API) -> None:
    response = test_client.set_stop_order(  # type: ignore
        ticker=faker.pystr(),
        stop_loss=faker.unique.random_int(),
        take_profit=faker.unique.random_int(),
    )

    assert json.loads(response.content.decode())["code"] == 4
    assert (
        "No matching pair is found for apiKey:"
        in json.loads(response.content.decode())["error"]
    )


def test_send_order(requests_mock: Mocker, test_client: API) -> None:
    with open("tests/responses/send_order.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}{ClientV2.path}", json=json_file)

        response = test_client.send_order(  # type: ignore
            ticker=faker.word(),
            side=faker.word(ext_word_list=sides.keys()),
            margin=faker.boolean(),
            count=faker.unique.random_int(),
            order_exp=faker.word(ext_word_list=[exp.value for exp in Expiration]),
            stop_price=faker.unique.random_int(),
        )

        assert json.loads(response.content.decode()) == json_file


def test_delete_order(requests_mock: Mocker, test_client: API) -> None:
    with open("tests/responses/delete_order.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}{ClientV2.path}", json=json_file)

        response = test_client.delete_order(order_id=faker.unique.random_int())  # type: ignore

        assert json.loads(response.content.decode()) == json_file


def test_get_ticker_info_sup_false(requests_mock: Mocker, test_client: API) -> None:
    with open("tests/responses/get_ticker_info_sup_false.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}", json=json_file)

        response = test_client.get_ticker_info(ticker="AMD")  # type: ignore

        assert json.loads(response.content.decode()) == json_file


def test_get_ticker_info_sup_true_weekday(
    requests_mock: Mocker, test_client: API
) -> None:
    with open("tests/responses/get_ticker_info_sup_true_weekday.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}", json=json_file)

        response = test_client.get_ticker_info(ticker="AMD", sup=True)  # type: ignore

        assert json.loads(response.content.decode()) == json_file


def test_get_ticker_info_sup_true_weekend(
    requests_mock: Mocker, test_client: API
) -> None:
    with open("tests/responses/get_ticker_info_sup_true_weekend.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}", json=json_file)

        response = test_client.get_ticker_info(ticker="AMD", sup=True)  # type: ignore

        assert json.loads(response.content.decode()) == json_file


def test_get_orders_active_only(requests_mock: Mocker, test_client: API) -> None:
    with open("tests/responses/get_orders_active_only.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}{ClientV2.path}", json=json_file)

        response = test_client.get_orders(active_only=True)  # type: ignore

        assert json.loads(response.content.decode()) == json_file


def test_get_orders(requests_mock: Mocker, test_client: API) -> None:
    with open("tests/responses/get_orders.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}{ClientV2.path}", json=json_file)

        response = test_client.get_orders()  # type: ignore

        assert json.loads(response.content.decode()) == json_file


def test_set_stop_order(requests_mock: Mocker, test_client: API) -> None:
    with open("tests/responses/set_stop_order.json") as file:
        json_file = json.load(file)

        requests_mock.post(f"{api_url}{ClientV2.path}", json=json_file)

        response = test_client.set_stop_order(  # type: ignore
            ticker="SONN", stop_loss=0.1, take_profit=1
        )

        assert json.loads(response.content.decode()) == json_file
