from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime
import requests


    
def html_mail_sender(subject, html_content, to, from_email=None):
    try:
        from django.core.mail import EmailMultiAlternatives

        if not from_email:
            from_email = "Digital A.H.M Packaging <" + settings.EMAIL_HOST_USER + ">"

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        return email.send()
    except Exception as e:
        print(e)
        return None
    


def forget_password_email_sender(user_name, user_otp, user_email):
    try:
        # print("--------------------")
        # print("user_name =",  user_name)
        # print("user_otp =",   user_otp)
        # print("user_email =", user_email)
        # print("--------------------")

        html_content = render_to_string('mail/forget_password_mail.html', {
            'user_full_name': user_name,
            'code': user_otp,
            'company_name': "Digital A.H.M Packaging",
        })

        html_mail_sender(
            'Recover your account.',    ## subject
            html_content,               ## html_content
            [user_email],               ## to
        )
        
        return 'success'
    except Exception as e:
        print(e)
        return 'error'
    
