import os


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "Cloud Asset Platform",
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cloud.db",
    )

    JWT_SECRET = os.getenv(
        "JWT_SECRET",
        "development-secret",
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development",
    )


settings = Settings()