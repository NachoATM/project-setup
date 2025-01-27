from dependency_injection import containers, provides
from app.authentication.dependency_injection.persistences.user_bo import UserBOPersistences
from app.authentication.domain.controllers.register import RegisterController
from app.authentication.api.router import token_database_dict

class RegisterControllers(containers.DeclarativeContainer):
    carlemany = provides.Singleton(
        RegisterController,
        user_database=UserBOPersistences.postgres(),


    )


