from app.config import DATABASE_URL, models

TORTOISE_ORM = {
    "connection": {"default": DATABASE_URL},
    "app":{
        "models":{
            "models": models,
            "default_connection": "default",
        },
    },

}