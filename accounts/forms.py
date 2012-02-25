from django import forms

class ProfileForm(forms.Form):
    location = forms.CharField()
    profile_picture = forms.ImageField()
