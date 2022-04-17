import datetime
import json

test_book_1 = {
    'id': 1001605784161,
    'title': 'Coffee Break Python Slicing',
    'subtitle': '24 Workouts to Master Slicing in Python, Once and for All',
    'price': 0.00,
    'rating': 0,
    'authors': 'Christian Mayer',
    'publisher': 'Self-publishing',
    'year': 2018,
    'pages': 89,
    'desc': 'Puzzle-based learning is an active learning technique. With code puzzles, you will learn faster, smarter, and better.Coffee Break Python Slicing is all about growing your Python expertise - one coffee at a time. The focus lies on the important slicing technique to access consecutive data ranges. Und...',
    'service_tag': 'python',
    'batch_datetime': '15.04.2022 17:59:44',
    'redeemed': False,
    'booking_datetime': '25.04.2022 17:59:44'
}

test_book_2 = {
    'id': 9781118678640,
    'title': 'Windows Azure Web Sites',
    'subtitle': '',
    'price': 4.50,
    'rating': 0,
    'authors': 'James Chambers',
    'publisher': 'Wrox',
    'year': 2013,
    'pages': 120,
    'desc': 'If you are looking for a straightforward, practical...',
    'service_tag': 'azure',
    'batch_datetime': '15.04.2022 17:59:44',
    'redeemed': False,
    'booking_datetime': '25.04.2022 17:59:44'
}

# Актуальная бронь на неделю
test_booking_1 = {
    'user_id': 1,
    'book_id': 1,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40,
                                          902733).strftime('%Y-%m-%d %H:%M:%S'),
    'expiry_datetime': datetime.datetime(2022, 4, 20, 14, 56, 40,
                                         902733).strftime('%Y-%m-%d %H:%M:%S'),
    'redeemed': False,
    'id': 1,
}

# Бронь с истекшим сроком бронирования
test_booking_2 = {
    'user_id': 1,
    'book_id': 2,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40,
                                          902733).strftime('%Y-%m-%d %H:%M:%S'),
    'expiry_datetime': datetime.datetime(2022, 4, 14, 12, 35, 17,
                                         506412).strftime('%Y-%m-%d %H:%M:%S'),
    'redeemed': False,
    'id': 2,
}

test_booking_3 = {
    'user_id': 2,
    'book_id': 2,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40,
                                          902733).strftime('%Y-%m-%d %H:%M:%S'),
    'expiry_datetime': datetime.datetime(2022, 4, 14, 12, 35, 17,
                                         506412).strftime('%Y-%m-%d %H:%M:%S'),
    'redeemed': False,
    'id': 3,
}


def test__on_get_book_info(client, books_service):
    book_id = 1001605784161

    params = {'book_id': book_id}
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    result = client.simulate_get(
        f'/api/books/book_info', params=params, headers=headers
    )

    assert result.status_code == 200
    assert result.json == test_book_1


def test__on_get_all_books(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    result = client.simulate_get(f'/api/books/all_books', headers=headers)

    assert result.status_code == 200
    assert result.json == [test_book_1, test_book_2]


def test__on_get_with_filters(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    params = {'authors': 'James Chambers', 'price': 'lt:10'}
    result = client.simulate_get(
        f'/api/books/with_filters', params=params, headers=headers
    )
    assert result.status_code == 200
    assert result.json == [test_book_2]


def test__on_post_create_booking(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    params = {'book_id': 9781118678640, 'user_id': 1, 'period': 4}
    result = client.simulate_post(
        f'/api/books/create_booking', body=json.dumps(params), headers=headers
    )
    assert result.status_code == 200


def test__on_get_booking_info(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    params = {
        'booking_id': 1,
    }

    result = client.simulate_get(
        f'/api/books/booking_info', params=params, headers=headers
    )
    assert result.status_code == 200
    assert result.json == test_booking_1


def test__on_get_show_all_booking(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    result = client.simulate_get(
        f'/api/books/show_all_booking', headers=headers
    )

    assert result.status_code == 200
    assert result.json == [test_booking_1, test_booking_2]


def test__on_post_delete_booking(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    params = {'book_id': 1001605784161}

    result = client.simulate_post(
        f'/api/books/delete_booking', body=json.dumps(params), headers=headers
    )

    assert result.status_code == 200


def test__on_post_redeem_booking(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    params = {'book_id': 1001605784161}

    result = client.simulate_post(
        f'/api/books/delete_booking', body=json.dumps(params), headers=headers
    )

    assert result.status_code == 200


def test__on_get_active_booking(client, books_service):
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdGluZ191c2VyXzEiLCJuYW1lIjoidGVzdGluZ19uYW1lXzEiLCJncm91cCI6IlVzZXIifQ.AzYtPz4F16sUu1ALSIzPUJeQM2AiZqfA-IpHcy-vNMI'
    }

    result = client.simulate_get(f'/api/books/active_booking', headers=headers)
    assert result.status_code == 200
    assert result.json == test_booking_1
