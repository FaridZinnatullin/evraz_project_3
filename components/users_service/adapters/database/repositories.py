from application import interfaces
from application.dataclasses import User
from sqlalchemy.sql import and_, select

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository


@component
class UsersRepo(BaseRepository, interfaces.UserRepo):

    def get_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def get_all(self):
        query = select(User)
        return self.session.execute(query).scalars().all()

    def add_instance(self, user: User):
        self.session.add(user)
        self.session.flush()
        return user

    def delete_by_id(self, user_id: int):
        user = self.get_by_id(user_id)
        self.session.delete(user)

    def update_by_id(self, user: User):
        pass

    def check_user_login(self, user_login: str):
        query = select(User).where(User.login == user_login)
        if self.session.execute(query).scalars().one_or_none():
            return True
        return False

    def authorization(self, login: str, password: str):
        query = select(User).where(
            and_(User.login == login, User.password == password)
        )
        return self.session.execute(query).scalars().one_or_none()
