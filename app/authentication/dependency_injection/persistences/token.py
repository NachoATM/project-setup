from dependency_injection import containers, provides
from app.authentication.persistence.memory_persistence.token import TokenMemoryPersistenceService
from app.authentication.persistence.redis_persistence.token import TokenRedisPersistenceService
from app.authentication.persistence.postgres_persistence.user_bo import UserBOPostgresPersistenceService

class TokenPersistences(containers.DeclarativeContainer):
    memory = provides.Singleton(
        TokenMemoryPersistenceService,
    )
    redis = provides.Singleton(
        TokenRedisPersistenceService,
    )
    carlemany = redis
