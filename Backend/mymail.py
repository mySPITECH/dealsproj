import os
from django.http import HttpResponse
from django.template import Context
from django.conf import settings
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage


class MAIL(object):

    def __init__(self, to,From,context,template,subject):
        self.to=[to]
        self.From =From
        ctx={'context':context}

        self.context=ctx
        self.template=template
        self.subject=subject
    
    def send_mail(self):
        subject=self.subject
        to=self.to
        from_email = settings.EMAIL_FROM
        context=self.context
        message =get_template(self.template).render(self.context)
        msg = EmailMessage(subject,message,to=to,from_email=from_email)
        msg.content_subtype="html"
        msg.send()
        print(msg)
        return msg
   