from django import forms
from .models import JobPosition, Profile

class ContactForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phoneNumber', 'linkedIn', 'instagram']

class JobPost(forms.ModelForm):
    class Meta:
        model=JobPosition
        fields=['title', 'location','salary', 'description']