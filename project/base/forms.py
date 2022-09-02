from django import forms

from django.forms import ModelForm
from .models import Group,Report,User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = "__all__"

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','group','email','password1','password2']

    def __init__(self,*args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        

class UserRegisterFormAdmin(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','group','email','password1','password2','is_superuser']

    def __init__(self,*args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2','is_superuser']:
            self.fields[fieldname].help_text = None
        
        
    
    
 