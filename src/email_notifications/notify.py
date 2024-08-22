from fastapi_mail import MessageSchema, MessageType, FastMail, ConnectionConfig

from config import templates_folder
from logger import logger

logger = logger

# Configuration for email sending using FastAPI Mail
conf = ConnectionConfig(
    MAIL_USERNAME="yardensepton",
    MAIL_PASSWORD="rxlw jlyl adcu miam",
    MAIL_FROM="yardensepton@email.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Easy Pack Support",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=templates_folder,
)


async def send_reset_password_mail(recipient_email, user, url, expire_in_minutes):
    """
    Sends a reset password email to the user with a link to reset their password.

    Args:
        recipient_email (str): The email address of the recipient.
        user (str): The username of the recipient.
        url (str): The URL for resetting the password.
        expire_in_minutes (int): The time in minutes for the reset link to expire.

    Raises:
        Exception: If there is an error while sending the email.
    """
    template_body = {
        "user": user,
        "url": url,
        "expire_in_minutes": expire_in_minutes
    }
    try:
        message = MessageSchema(
            subject="Easy Pack - Reset Password",
            recipients=[recipient_email],
            template_body=template_body,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password_email.html")
    except Exception as e:
        logger.error(f"Error sending email notification: {e}")
        raise Exception(f"Error sending email notification: {e}")
    logger.info(f"Email was sent successfully to {recipient_email}")

