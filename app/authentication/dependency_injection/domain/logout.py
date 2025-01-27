from dependency_injection import containers, provides
from app.authentication.dependency_injection.persistences.user_bo import UserBOPersistences
from app.authentication.domain.controllers.logout import LogoutController
from app.authentication.api.router import token_database_dict

class LogoutControllers(containers.DeclarativeContainer):
    carlemany = provides.Singleton(
        LogoutController,
        user_database=UserBOPersistences.memory,


    )


