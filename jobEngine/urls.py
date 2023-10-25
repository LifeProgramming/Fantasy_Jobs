from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('jobs/', views.jobListView, name='jobs'),
    path('job-detail/<int:pk>', views.jobDetail, name='job-detail'),
    path('contacts/<int:pk>', views.Contacts, name='contacts'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register-job-seeker/', views.registerUser, name='register'),
    path('register-recruiter/', views.registerRcruiter, name='recruiter'),
    path('searches/', views.searchJobs, name='search'),
    path('contact-form/', views.postContact, name='contact'),
    path('contact-edit/', views.updateContact, name='update-contact'),
    path('contact-delete/', views.deleteContact, name='delete-contact'),
    path('posted-jobs/', views.postedJobs, name='posted-jobs'),
    path('job-post/',views.newJob, name='new-job'),
    path('edit-job/<int:pk>', views.updateJob, name='update-job'),
    path('delete-job/<int:pk>', views.deleteJob, name='delete-job'),
]