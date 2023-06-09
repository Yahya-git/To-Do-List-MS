from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from src.config import settings
from src.dtos import dto_misc

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_tls,
    MAIL_SSL_TLS=settings.mail_ssl,
    USE_CREDENTIALS=settings.use_credentials,
)


async def send_mail(email: dto_misc.EmailList, subject_template: str, template: str):
    message = MessageSchema(
        subject=subject_template, recipients=[email], body=template, subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
