import faker
import pytest
from faker import Faker

from tradernet_api.api import API

fake = Faker()


@pytest.fixture
def test_client() -> API:
    """
    Test client fixture with random fake api and secret keys.

    :return: API
    """
    return API(api_key=fake.pystr(), secret_key=fake.pystr())
