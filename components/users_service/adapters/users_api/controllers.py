import jwt
import os

import jwt
from evraz.classic.components import component
from evraz.classic.http_auth import (
    authenticator_needed,
    authenticate
)

from application import services
from .join_points import join_point


@authenticator_needed
@component
class Users:
    users_manager: services.UsersManager


    @join_point
    @authenticate
    def on_get_user_info(self, request, response):
        request.params['user_id'] = int(request.context.client.user_id)
        user = self.users_manager.get_user_by_id(**request.params)
        result = {
            'user_id': user.id,
            'user_login': user.login,
            'user_name': user.name
        }
        response.media = result

    @join_point
    def on_post_registration(self, request, response):
        self.users_manager.registration(**request.media)

    @join_point
    def on_post_login(self, request, response):
        user = self.users_manager.login(**request.media)
        secret_jwt_key = os.getenv('SECRET_JWT_KEY')
        token = jwt.encode(
            {
                "sub": user.id,
                "login": user.login,
                "name": user.name,
                "group": "User"
            },
            secret_jwt_key,
            algorithm="HS256"
        )
        response.media = {
            "token": token
        }
