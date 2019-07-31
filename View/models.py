import sys
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from PIL import Image
from django.conf import settings
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
class Profile(models.Model):
    state = models.CharField(null=True,blank=True, max_length=50)
    city = models.CharField(null=True,blank=True, max_length=50)
    mobile_no = models.CharField(null=False,blank=False, max_length=50,)
    address= models.CharField( max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='user/%d/%m/%y', null=True, 
                            blank=True,default=settings.AVARTA)
    gender = models.CharField(null=True,blank=True, max_length=50)
    education= ArrayField(models.CharField(null=True,blank=True, max_length=50),
                      null=True,blank=True)
    work=models.CharField(null=True,blank=True, max_length=50)
    about = models.TextField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Profile, self).save(*args, **kwargs)
    def compressImage(self,image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=80)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.*" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image
    def __str__(self):
        return self.state
    class Meta:
        permissions=(("is_staff","A staff"),)
                    
    def get_absolute_url(self):
        return reverse("profile_detail", args=str([self.id]))
class Cleanser(models.Model):
    names = models.CharField(blank=True,null=True, max_length=50)
    image = models.ImageField( upload_to='cleanser/%d/%m/%y')
    address= models.CharField( max_length=50,blank=True,null=True)
    state= models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField( max_length=50,blank=True,null=True)
    mobile_no = models.CharField(max_length=50,blank=True,null=True)
    token = models.CharField(blank=True,null=True,max_length=50)
    def get_absolute_url(self):
        return reverse("cleanser-detail",args=str([self.id]) )
class Category(models.Model):
       name = models.CharField( max_length=50)
       op = models.ForeignKey(User, on_delete=models.CASCADE)
       date = models.DateTimeField( auto_now=True, auto_now_add=False)
class Deals(models.Model):
    title = models.CharField( max_length=50)
    token = models.CharField(blank=True,null=True, max_length=50)
    about = models.TextField(max_length=120)
    op = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    status = models.BooleanField(default=False)
    framework = ArrayField(models.CharField(max_length=50))
    is_valid = models.BooleanField(default=False)
    moderator = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateTimeField( auto_now=True, auto_now_add=False)
    views = models.IntegerField(blank=True, null=True,default=0)
    is_verified = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return self.op
        class META:
            ordering = ['date','title']
    def get_absolute_url(self):
        return reverse("deal_detail", args=str([self.slug]))
class Mydeals(models.Model):
    deal_code= models.CharField( max_length=50,blank=True,null=True)
    deal_id = models.ForeignKey(Deals, on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(blank=True,null=True,max_length=50)
    owner= models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(max_length=50,default="pending")
    is_fufilled = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_fufiled = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self):
        return self.user
class Request(models.Model):
    title = models.CharField(max_length=50)
    op = models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    text = models.CharField( max_length=50)
    def __str__(self):
        return self.user
class Message(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    files = models.FileField(blank=True,null=True,upload_to="message/%d/%m/%y", max_length=50)
class Reply(models.Model):
    text = models.TextField()
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    files = models.FileField(blank=True,null=True, upload_to="reply/%d/%m/%y", max_length=100)
class Payment(models.Model):
    payee = models.ForeignKey(User, on_delete=models.CASCADE)
    deal_code = models.CharField( max_length=50)
    bank = models.CharField( max_length=50)
    amount = models.CharField( max_length=50)
    teller= models.ImageField( upload_to="teller/%d/%m/%y", max_length=50)
class Review(models.Model):
    text =models.TextField()
    stars= models.BigIntegerField()
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE)
    op = models.ForeignKey(User, on_delete=models.CASCADE)


