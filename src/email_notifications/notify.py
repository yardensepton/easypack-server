from fastapi_mail import MessageSchema, MessageType, FastMail, ConnectionConfig

from config import templates_folder

conf = ConnectionConfig(
    MAIL_USERNAME="yardensepton",
    MAIL_PASSWORD="rxlw jlyl adcu miam",
    MAIL_FROM="yardensepton@email.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="EasyPack Developers",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=templates_folder,
)


async def send_reset_password_mail(recipient_email, user, url, expire_in_minutes):
    template_body = {
        "user": user,
        "url": url,
        "expire_in_minutes": expire_in_minutes
    }
    try:
        message = MessageSchema(
            subject="EasyPack - Reset Password",
            recipients=[recipient_email],
            template_body=template_body,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password_email.html")
    except Exception as e:
        raise Exception(f"Error sending email notification: {e}")
        # logger.error(f"Something went wrong in reset password email")
        # logger.error(str(e))
