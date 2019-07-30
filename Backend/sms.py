import os
import requests
from django.http import HttpResponse
from django.template import Context
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage


class SMS:
    
    

    def __init__(self,message,number):
        self.message=message
        self.number=number
    
    def send_message(self):
        URL= settings.SMS_URL
        USERNAME= settings.SMS_USERNAME
        PASSWORD = settings.SMS_PASSWORD
        SENDER_ID = settings.SMS_SENDER_ID
        payload={"username":USERNAME,"password":PASSWORD, "sender":SENDER_ID,"recipient":self.number,"message":self.message}
        MESSAGE = requests.get(URL,params=payload)
        STATUS = MESSAGE.status_code
        print(MESSAGE.url)
        print(STATUS) 
        return MESSAGE
