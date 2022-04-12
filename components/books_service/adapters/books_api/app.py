from typing import Tuple, Union

from evraz.classic.http_api import App
from evraz.classic.http_auth import Authenticator

from application import services
from . import auth, controllers


def create_app(books_manager: services.BooksManager, ) -> App:

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    authenticator.set_strategies(auth.jwt_strategy)
    app = App(prefix='/api')
    app.register(controllers.Books(authenticator=authenticator, books_manager=books_manager))
    return app
