from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User


class UserRepo(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def add_instance(self, user_data):
        pass

    @abstractmethod
    def delete_by_id(self, user_id: int):
        pass

    @abstractmethod
    def check_user_login(self, user_login: Optional[str]) -> bool:
        pass

    @abstractmethod
    def update_by_id(self, user: User):
        pass

    @abstractmethod
    def authorization(self, login: str, password: str):
        pass


