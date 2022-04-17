import pytest
from attr import asdict
from components.books_service.application import errors, services


@pytest.fixture(scope='function')
def service_book_updater(books_repo, publisher):
    return services.BooksUpdaterManager(books_repo=books_repo, publisher=publisher)


data_book = {
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
    'redeemed': False
}

data_book_1 = {
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
    'redeemed': False
}

data_book_3 = {
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
    'booking_datetime': None
}


def test_create_and_get(service_book_updater):
    book = service_book_updater.create_and_get(book_id=data_book['id'], service_tag=data_book['service_tag'],
                                               batch_datetime=data_book['batch_datetime'])
    assert asdict(book) == data_book_3


def test_create_and_get_download_error(service_book_updater):
    uncorrected_id = '00000'
    with pytest.raises(errors.DownloadError):
        service_book_updater.create_and_get(book_id=uncorrected_id, service_tag=data_book['service_tag'],
                                            batch_datetime=data_book['batch_datetime'])


def test_add_books_package(service_book_updater):
    books_package = [data_book, data_book_1]
    service_book_updater.add_books_package(books_package)
    service_book_updater.books_repo.add_instance_package.assert_called_once()


def test_send_top_books(service_book_updater):
    tags = ['delphi']
    batch_datetime = '15.04.2022 17:59:44'

    service_book_updater.send_top_books(tags, batch_datetime)
    service_book_updater.books_repo.get_top_by_tag.assert_called_once()


def test_get_tag_from_rabbit(service_book_updater):
    book_tags = ['delphi']
    batch_datetime = '15.04.2022 17:59:44'

    assert service_book_updater.get_tag_from_rabbit(book_tags, batch_datetime) == None

def test_get_by_pages(service_book_updater):
    page_num = 2
    book_tag = 'delphi'
    batch_datetime = '15.04.2022 17:59:44'

    service_book_updater.get_by_pages(page_num=page_num,
                                      book_tag=book_tag,
                                      batch_datetime=batch_datetime)

    service_book_updater.books_repo.add_instance_package.assert_called_once()

def test_get_tag_from_rabbit_async(service_book_updater):
    book_tags = ['delphi']
    batch_datetime = '15.04.2022 17:59:44'

    assert service_book_updater.get_tag_from_rabbit_async(book_tags, batch_datetime) == None






