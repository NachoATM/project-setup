from dependency_injection import containers, provides
from app.authentication.persistence.memory_persistence.user_bo import UserBOMemoryPersistenceService
from app.authentication.persistence.postgres_persistence.user_bo import UserBOPostgresPersistenceService

class UserBOPersistences(containers.DeclarativeContainer):
    memory = provides.Singleton(
        UserBOMemoryPersistenceService,
    )

    postgres = provides.Singleton(
        UserBOPostgresPersistenceService,
    )


