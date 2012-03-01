from django import forms

class ProfileForm(forms.Form):
    location = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)
