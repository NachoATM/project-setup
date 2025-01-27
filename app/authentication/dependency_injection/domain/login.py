from dependency_injection import containers, provides
from app.authentication.dependency_injection.persistences.user_bo import UserBOPersistences
from app.authentication.domain.controllers.login import LoginController
from app.authentication.api.router import token_database_dict

class LoginControllers(containers.DeclarativeContainer):
    carlemany = provides.Singleton(
        LoginController,
        user_database=UserBOPersistences.postgres(),
        token_database=token_database_dict,

    )


