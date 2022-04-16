from unittest.mock import Mock

import pytest
from falcon import testing

from components.users_service.adapters import users_api
from components.users_service.application import services, dataclasses

@pytest.fixture(scope='function')
def user():
    return dataclasses.User(
        id=1,
        name='user1',
        login=None,
        password=None
    )


@pytest.fixture(scope='function')
def user_1():
    return dataclasses.User(
        id=2,
        name='user2',
        login=None,
        password=None
    )

@pytest.fixture(scope='function')
def user_2():
    return dataclasses.User(
        id=1,
        name='user1',
        login='user1',
        password='password1'
    )


@pytest.fixture(scope='function')
def users_service(user, user_1, user_2):
    users_service = Mock(services.UsersManager)
    users_service.get_all_users = Mock(return_value=None)
    users_service.get_user_by_id = Mock(return_value=user_2)
    users_service.registration = Mock(return_value=None)
    users_service.login = Mock(return_value=user_2)
    return users_service


# @pytest.fixture(scope='function')
# def catalog_service(product_1):
#     service = Mock(services.Catalog)
#     service.get_product = Mock(return_value=product_1)
#
#     return service
#
#
# @pytest.fixture(scope='function')
# def orders_service():
#     service = Mock(services.Orders)
#
#     return service
#
#
# @pytest.fixture(scope='function')
# def customers_service():
#     service = Mock(services.Customers)
#
#     return service


@pytest.fixture(scope='function')
def client(users_service):
    app = users_api.create_app(
        users_manager=users_service,
    )

    return testing.TestClient(app)
