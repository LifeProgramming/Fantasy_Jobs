from django.contrib import admin
from .models import Profile, JobPosition, SavedJobs
from .models import JobSeeker, JobExperience,EducationExperience,Skill

# Register your models here.
admin.site.register(Profile)
admin.site.register(JobPosition)
admin.site.register(JobSeeker)
admin.site.register(JobExperience)
admin.site.register(EducationExperience)
admin.site.register(Skill)
