from evraz.classic.app.errors import AppError


class NoPermission(AppError):
    msg_template = "You have no permissions to perform this action"
    code = 'users.no_permissions'


class UserAlreadyExist(AppError):
    msg_template = "This login is already occupied"
    code = 'users.user_already_exist'


class UncorrectedParams(AppError):
    msg_template = "You give me very bad params... I have no data for you"
    code = 'users.bad_params'


class UncorrectedLoginPassword(AppError):
    msg_template = "Incorrect username or password"
    code = 'users.authorization'
