from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import random

from mailing.web.template import template


def send_code(to, guildName, SENDGRID_KEY) -> int:
    """
    Sends the auth code to the user
    """
    code = f"{guildName[:3].upper()}{random.randint(1000, 9999)}"

    subject = f"Your verification code is {code}"

    html = template(code)

    message = Mail(
        from_email="checkmate@devtranet.tech",
        to_emails=to,
        subject=subject,
        html_content=html,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        sg.send(message)

        return code
    except:
        raise Exception("Could not send the email...")
