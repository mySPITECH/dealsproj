from .models import Profile,Deals
from django.forms import ModelForm
from django.contrib.auth.models import User

class ProfileForm(ModelForm):

    class META:
        fields = '__all__'
        model= Profile

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['is_staff','is_supperuser','is_active','date_joined']
    