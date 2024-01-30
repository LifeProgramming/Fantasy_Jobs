from django import forms
from .models import JobPosition, Profile,JobSeeker,JobExperience, Skill,EducationExperience

class ContactForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phoneNumber', 'linkedIn', 'instagram']

class JobPost(forms.ModelForm):
    class Meta:
        model=JobPosition
        fields=['title', 'location','salary', 'description']

class JobSeekerProfile(forms.ModelForm):
    class Meta:
        model=JobSeeker
        fields=['name', 'job_name','phone_number','email','summary']

class EducationForm(forms.ModelForm):
    class Meta:
        model=EducationExperience
        fields=['education_name','university_name','started_date','finished_date']

class JobExperienceForm(forms.ModelForm):
    class Meta:
        model=JobExperience
        fields=['job_name','company_name','started_date','finished_date','description']

class SkillForm(forms.ModelForm):
    class Meta:
        model=Skill
        fields=['skill_name']