from django.conf import settings 
# html email required stuff

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from official.models import * 


def send_forget_password_mail(email , token):
    html_content = render_to_string("user/email.html",{'title':'send mail','content':token})
    text_content = strip_tags(html_content)
    subject = 'We have received a request to reset your password.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()


def payment_mail(id):
    payment_details = FranchiseWallet.objects.filter(id=id).first()
    html_content = render_to_string("official/payment-mail.html",{'title':'send mail','content':payment_details})
    text_content = strip_tags(html_content)
    subject = 'account credited'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [payment_details.franchise.email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()