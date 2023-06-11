from pydantic import BaseSettings


class Settings(BaseSettings):
    url: str
    users_service_url: str
    tasks_service_url: str
    secret_key: str
    algorithm: str
    access_token_expire_time: int
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: str
    mail_server: str
    mail_tls: bool
    mail_ssl: bool
    use_credentials: bool
    google_client_id: str
    google_client_secret: str
    redirect_url: str
    cache_expiry_time: int

    class Config:
        env_file = ".env"


settings = Settings()
