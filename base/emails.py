# import imp
from django.conf import settings
from django.core.mail import send_mail




def send_account_activation_email(email , email_token):
    print("In send_account_activation_email")
    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    print("email form: "+email_from)
    print("email to: "+email)
    message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    send_mail(subject , message , email_from , [email], False)
    return