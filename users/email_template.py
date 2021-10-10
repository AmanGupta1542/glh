
from django.core.mail import send_mail , EmailMessage
from django.conf import settings

def send_email(user_email , token):
    message = "<a href='http://127.0.0.1:8000/user/rocovery-template/{token}/'>Click here to reset password</a>".format(token = token)



    subject = "Recover Password"
    email = EmailMessage(subject , message ,settings.EMAIL_HOST_USER,[user_email])
    email.content_subtype = 'html'

    send = email.send()
    if send:
        return True
    else :
        return False
