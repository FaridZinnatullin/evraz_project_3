import pytest
from attr import asdict

from components.users_service.application import errors, services


@pytest.fixture(scope='function')
def service_user(users_repo, publisher):
    return services.UsersManager(users_repo=users_repo, publisher=publisher)


data_user = {'id': 1, 'name': 'user1', 'login': None, 'password': None}

data_user_auth = {
    'id': 1,
    'name': 'user1',
    'login': 'user1',
    'password': 'password1'
}

data_user_registration = {
    'name': 'user1',
    'login': 'login1',
    'password': 'password1',
}

data_user2 = {'id': 2, 'name': 'user2', 'login': None, 'password': None}


def test_registration_already_exist(service_user):
    with pytest.raises(errors.UserAlreadyExist):
        service_user.registration(**data_user_registration)


def test_registration(service_user, users_repo):
    user = users_repo.get_none_user()
    users_repo.check_user_login.return_value = user

    service_user.registration(**data_user_registration)
    service_user.users_repo.add_instance.assert_called_once()


def test_get_user_by_id(service_user):
    user = service_user.get_user_by_id(data_user['id'])
    assert asdict(user) == data_user


def test_get_user_by_id_uncorrected_params(service_user, users_repo):
    none_user = users_repo.get_none_user()
    users_repo.get_by_id.return_value = none_user

    with pytest.raises(errors.UncorrectedParams):
        service_user.get_user_by_id(data_user['id'])


def test_get_all_user(service_user):
    users = service_user.get_all_users()
    users = [asdict(user) for user in users]
    assert users == [data_user, data_user2]


def test_delete_user(service_user):
    service_user.delete_user(user_id=data_user['id'])
    service_user.users_repo.delete_by_id.assert_called_once()


def test_login(service_user):
    user = service_user.login(
        login=data_user_auth['login'], password=data_user_auth['password']
    )
    assert asdict(user) == data_user_auth


def test_login_uncorrected_login_password(service_user, users_repo):
    none_user = users_repo.get_none_user()
    users_repo.authorization.return_value = none_user

    with pytest.raises(errors.UncorrectedLoginPassword):
        service_user.login(
            login=data_user_auth['login'], password=data_user_auth['password']
        )
