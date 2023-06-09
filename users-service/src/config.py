from pydantic import BaseSettings


class Settings(BaseSettings):
    url: str
    tasks_service_url: str
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str
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

    class Config:
        env_file = ".env"


settings = Settings()
