import pytest
from sqlalchemy.orm import registry

from components.users_service.adapters.database import tables
from components.users_service.adapters.database.repositories import UsersRepo
from components.users_service.application.dataclasses import User


@pytest.fixture(scope='function')
def fill_db(session):
    users_data = [
        {
            'name': 'test_name',
            'login': 'test_login',
            'password': 'test_password',
        },
        {
            'name': 'test_name_1',
            'login': 'test_login_1',
            'password': 'test_password_1',
        },
    ]

    session.execute(tables.users.insert(), users_data)


@pytest.fixture(scope='function')
def mapping():
    mapper = registry()
    mapper.map_imperatively(User, tables.users)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return UsersRepo(context=transaction_context)


def test__check_user_login(repo, fill_db):
    result = repo.check_user_login(user_login='test_login')
    assert result == True


def test__get_by_id(repo, fill_db):
    users = repo.get_all()
    first_user = users[0]
    user = repo.get_by_id(user_id=first_user.id)

    assert user.id == first_user.id


def test__get_all(repo, fill_db):
    users = repo.get_all()
    assert len(users) != 0


def test__add_instance(repo, fill_db, mapping):
    user_data = User(
        name='test_name_for_test',
        login='test_login_for_test',
        password='test_login_for_test',
    )

    user = repo.add_instance(user_data)

    assert user.id != None


def test__delete_by_id(repo, fill_db):
    users = repo.get_all()
    first_user = users[0]

    result = repo.delete_by_id(first_user.id)

    assert result == None


def test__authorization(repo, fill_db):
    test_data = {
        'login': 'test_login',
        'password': 'test_password'
    }
    user = repo.authorization(login=test_data['login'],
                              password=test_data['password'])

    assert user != None
    assert user.id != None

