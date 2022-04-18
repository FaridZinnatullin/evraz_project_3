from unittest.mock import Mock

import pytest

from evraz.classic.messaging import Publisher

from components.users_service.application import dataclasses, interfaces


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(id=1, name='user1', login=None, password=None)


@pytest.fixture(scope='function')
def user_1():
    return dataclasses.User(id=2, name='user2', login=None, password=None)


@pytest.fixture(scope='function')
def user_2():
    return dataclasses.User(
        id=1, name='user1', login='user1', password='password1'
    )


@pytest.fixture(scope='function')
def users_repo(user, user_1, user_2):
    users_repo = Mock(interfaces.UserRepo)
    users_repo.get_user = Mock(return_value=user)
    users_repo.get_by_id = Mock(return_value=user)
    users_repo.authorization = Mock(return_value=user_2)
    users_repo.get_all = Mock(return_value=[user, user_1])
    users_repo.get_none_user = Mock(return_value=None)
    return users_repo


@pytest.fixture(scope='function')
def publisher():
    publisher = Mock(Publisher)
    return publisher
