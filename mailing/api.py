from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import random

from mailing.web.template import template


API_KEY = "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"


def send_code(to, guildName) -> int:
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
        sg = SendGridAPIClient(API_KEY)
        sg.send(message)

        return code
    except:
        raise Exception("Could not send the email...")
