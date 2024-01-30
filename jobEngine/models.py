from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200)
    phoneNumber = models.CharField(max_length=100)
    linkedIn = models.CharField(max_length=1000, null=True, blank=True)
    instagram = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username 








class JobSeeker(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    job_name = models.CharField(max_length=100, verbose_name='Job Title')

    # Contact Information
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()

    summary = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Job Seeker'
        verbose_name_plural = 'Job Seekers'

    def __str__(self):
        return self.name

class JobExperience(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='job_experiences', default=None)
    job_name = models.CharField(max_length=100)
    company_name=models.CharField(max_length=200, default='')
    started_date = models.CharField(max_length=200)
    finished_date = models.CharField(blank=True, null=True, max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Job Experience'
        verbose_name_plural = 'Job Experiences'

    def __str__(self):
        return f"{self.job_seeker.name} - {self.job_name}"

class EducationExperience(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='education_experiences', default=None)
    education_name = models.CharField(max_length=100)
    university_name = models.CharField(max_length=150)
    started_date = models.CharField(max_length=200)
    finished_date = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Education Experience'
        verbose_name_plural = 'Education Experiences'

    def __str__(self):
        return f"{self.job_seeker.name} - {self.education_name}"

class Skill(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='skills', default=None)
    skill_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f"{self.job_seeker.name} - {self.skill_name}"

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200, null=True, blank=True)
    salary = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=10000)
    posted_by = models.ForeignKey("Profile", on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=timezone.now)
    applied_persons=models.ManyToManyField(JobSeeker, null=True, blank=True)
   
    
   

    def __str__(self):
        return self.title  
    

class SavedJobs(models.Model):
    saver=models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    job=models.ForeignKey(JobPosition, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.title