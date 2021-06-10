from flask import (
    current_app,
)
from .constants import (
    APP_NAME,
    MESSAGES,
    SERIALIZER_LOADS_MAX_AGE,
)
from .generators import (
    create_recovery_token,
)
from flask_mail import (
    Mail,
    Message,
)
from threading import Thread
#from generators import recovery_generator

mail = Mail()


def create_recovery_account_data(user):
    key = create_recovery_token(user)
    link = f"{current_app.config['FRONTEND_ENDPOINT']}"
    recipients = [user.email]
    recovery_link = f"{link}/auth/reset?key={key}"
    subject = f"Account Recovery - {APP_NAME}"
    body = f"Hi {user.username.upper()}! Your Recovery Link is: {recovery_link}"
    html = f'<html><body><b>Hi {user.username.upper()},</b><br/><br/>' + \
        f'<b>Please</b>' + \
        f'<a href="{recovery_link}">' + \
        f' click this link</a> to recover/reset your account password.' + \
        f'<br/><br/> If you can\'t click the link from your email program,' + \
        f'please copy the this URL and paste it into your web browser:<br/>' + \
        f'<br/> {recovery_link}<br/><br/><br/>' + \
        f'This Link will expired in the next <b>{int(SERIALIZER_LOADS_MAX_AGE / (60*60))} hours</b><br/>' + \
        f'<br/><br/><b>If you didn\'t request for this email, please ignore.</b><br/><br/>' + \
        f'Cheers,<br/><br/></br> <a href="{link}">{APP_NAME} Team</a><br/>' + \
        f'</body></html>'

    return {"subject": subject, "body": body, "html": html, "recipients": recipients}


def send_msg_async(msg, app):
    with app.app_context():
        try:
            print(msg)
            mail.send(msg)
        except Exception as e:
            print(f"Error from Email: ", e)


def send_msg(user, app):
    try:
        data = create_recovery_account_data(user)
        subject = data["subject"]
        body = data["body"]
        html = data["html"]
        recipients = data["recipients"]

        msg = Message(subject, recipients=recipients, body=body, html=html)
        #t = Thread(target=send_msg_async, args=(msg, app))
        # t.start()
        # t.join()
        send_msg_async(msg, app)

        return True

    except Exception as e:
        print(f'error: {e}')
        return False
