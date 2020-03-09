from django import forms
class LoginField(forms.Form):
    username=forms.CharField(required=True,max_length=50)
    password=forms.CharField(required=True,min_length=3)
