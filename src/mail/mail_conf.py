from fastapi_mail import ConnectionConfig
import os


class Environ:
    """
    Клас для зберігання конфігурації електронної пошти, завантаженої з змінних середовища.
    """
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_TLS = os.getenv("MAIL_TLS", "True") == "True"
    MAIL_SSL = os.getenv("MAIL_SSL", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY")


conf = ConnectionConfig(

    MAIL_USERNAME = Environ.MAIL_USERNAME,
    MAIL_PASSWORD = Environ.MAIL_PASSWORD,
    MAIL_FROM = Environ.MAIL_FROM,
    MAIL_PORT = Environ.MAIL_PORT,
    MAIL_SERVER = Environ.MAIL_SERVER,
    MAIL_TLS = Environ.MAIL_TLS,
    MAIL_SSL = Environ.MAIL_SSL,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
