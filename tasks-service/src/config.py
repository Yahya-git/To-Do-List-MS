from pydantic import BaseSettings


class Settings(BaseSettings):
    url: str
    users_service_url: str
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: str
    mail_server: str
    mail_tls: bool
    mail_ssl: bool
    use_credentials: bool
    max_tasks: int
    cache_expiry_time: int

    class Config:
        env_file = ".env"


settings = Settings()
