##EVRAZ Project 3

Данный проект является реализацией поставленной <a href = 'https://docs.google.com/document/d/1hOBwmUPiBxQrhuyJUFoKR86qHjz9F02AH3d9WUe_CMQ'>задачи</a>,
в рамках прохождения совместного буткемпа от ЕВРАЗа и Алгоритмики.

###Архитектура
Приоритетным условием задачи являлась реализация на основе микросервисной,
а также чистой и гексагональной архитектуры.

###Документация
Основная документация проекта находится в директории `/components/docs`

###Библиотеки и технологии
<a href='https://nginx.org/ru/'>Nginx</a> - проксирование и балансировка

<a href='https://rabbitmq.com/'>RabbitMQ</a> - брокер сообщений для микросервисного взаимодействия

<a href='https://www.docker.com/'>Docker</a> - развертывание проекта

<a href='https://www.postgresql.org/'>PostgreSQL</a> - база данных

<a href='https://falconframework.org/'>Falcon</a> - основной web-фреймворк

<a href='https://www.sqlalchemy.org/'>SQLAlchemy</a> - ОРМ приложения

<a href='https://docs.pytest.org/en/7.1.x/'>PyTest</a> - тестирование

С другими используемыми пакетами можно ознакомиться в файле `config.cfg`.

Также были использованы python-пакеты, являющиеся собственностью компании <a href='https://www.evraz.com/en/'>ЕВРАЗ</a>

###Структура
Основой приложения являются 2 микросервиса `Users` и `Books`

###Развертывание и запуск
````
git clone https://github.com/FaridZinnatullin/evraz_project_3.git
cd ./components
docker-compose up --build
````
Для заполнения базы данных книгами:  

`docker exec -t components_books_service_1 bash -c "books_service get-books [tags]"`,
где `[tags]` - ключевые слова для поиска книг, записанные через пробел 

###Переменные окружения
Все переменные окружения, используемые в приложении находятся в файле docker-compose.yaml

### URL для запросов
- Для сервиса `Users (сервис пользователей)`:
    - `POST 127.0.0.1/api/users/registration` регистрация пользователя
    - `POST 127.0.0.1/api/users/login` авторизация пользователя (для получения токена)
    - `GET 127.0.0.1/api/users/user_info` получение информации о себе
- Для сервиса `Books (сервис книг)`:
    - `GET 127.0.0.1/api/books/book_info` получение подробной информации о книге
    - `GET 127.0.0.1/api/books/all_books` получение общего каталога с книгами
    - `GET 127.0.0.1/api/books/with_filters` получение списка книг, соответствующих указанным фильтрам
    - `POST 127.0.0.1/api/books/create_booking` забронировать книгу
    - `GET 127.0.0.1/api/books/booking_info` получить информацию о брони
    - `GET 127.0.0.1/api/books/show_all_booking` получить список броней пользователя
    - `POST 127.0.0.1/api/books/delete_booking` удалить бронь
    - `POST 127.0.0.1/api/books/redeem_booking` выкупить бронь
    - `GET 127.0.0.1/api/books/active_booking` получить активную бронь (если имеется)
    
