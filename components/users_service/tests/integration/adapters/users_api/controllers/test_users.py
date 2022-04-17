import json


def test__on_get_user_info(client, users_service):
    user_id = 1
    expected = {
        'user_id': 1,
        'user_login': 'user1',
        'user_name': 'user1',
    }
    params = {'user_id': user_id}
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    result = client.simulate_get(
        f'/api/users/user_info', params=params, headers=headers
    )

    assert result.status_code == 200
    assert result.json == expected


def test__on_post_registration(client, users_service):
    user_media = {
        'login': 'user1',
        'password': 'password1',
        'name': 'user1',
    }
    result = client.simulate_post(
        f'/api/users/registration', body=json.dumps(user_media)
    )

    assert result.status_code == 200


def test__on_post_login(client, users_service):
    user_media = {
        'login': 'user1',
        'password': 'password1',
    }
    result = client.simulate_post(
        f'/api/users/login', body=json.dumps(user_media)
    )

    assert result.status_code == 200
    result = result.json
    assert result.get('token') is not None
