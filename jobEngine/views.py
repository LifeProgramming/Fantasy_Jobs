from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import JobPosition, Profile, SavedJobs,JobSeeker,JobExperience,EducationExperience,Skill
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import authenticatedUser, allowed_users,profileMaking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group 
from .forms import ContactForm, JobPost, JobSeekerProfile,EducationForm,JobExperienceForm,SkillForm


# Create your views here.


@authenticatedUser
def loginUser(request):
    page='login'
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            return HttpResponse('Sorry! This user does not exist!!!')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            group=request.user.groups.all()[0].name
            if group=='Recruiter':
                return redirect('posted-jobs')
            else:
                return redirect('j-home')
        else:
            return HttpResponse('Sorry! Something went wrong!!!')
        
    context={
        'page':page,
    }
    return render(request,'authentications.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')



def registerUser(request):
    page='job_seeker'
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='Job_Seeker')
            user.groups.add(group)
            login(request,user)
            return redirect('profile')
        else:
            return HttpResponse('Sorry! Something went wrong!!!')
    context={'form':form, 'page':page}
    return render(request, 'authentications.html', context)


def registerRcruiter(request):
    page='login'
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='Recruiter')
            user.groups.add(group)
            login(request,user)
            return redirect('contact')
        else:
            return HttpResponse('Sorry! Something went wrong!!!')
    context={'form':form, 'page':page}
    return render(request, 'recruiter_auth.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Recruiter'])
def postContact(request):
    if request.method == 'POST':
    
        
            form = ContactForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('posted-jobs')  
    else:
        form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'contacts_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Recruiter'])
def updateContact(request):
    update_item = Profile.objects.get(user=request.user)
    if request.user!= update_item.user:
        return HttpResponseForbidden('Sorry! You are not allowed to change this user!')


    if request.method == 'POST':
        form = ContactForm(request.POST or None, instance=update_item)
        if form.is_valid():
            form.save()
        return redirect('posted-jobs')  
    else:
        form = ContactForm(instance=update_item)

    context = {
        'form': form,
    }
    return render(request, 'contacts_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def postedJobs(request):
    if not Profile.objects.get(user=request.user):
        return redirect('contact')
    user=Profile.objects.get(user=request.user)
    p=Paginator(JobPosition.objects.filter(posted_by=user), 5)
    page=request.GET.get('page')
    items=p.get_page(page)
    context={
        'items':items,
    }
    return render(request, 'postedJobs.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def deleteContact(request):
    update_item = Profile.objects.get(user=request.user)
    if request.user!= update_item.user:
        return HttpResponseForbidden('Sorry! You are not allowed to change this user!')
    object=Profile.objects.get(user=request.user)
    object.delete()
    return redirect('contact')

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Recruiter'])
def newJob(request):
    if not Profile.objects.get(user=request.user):
        return redirect('contact')
    recruiter=Profile.objects.get(user=request.user)
    if request.method=='POST':
        form=JobPost(request.POST or None)
        if form.is_valid():
            form=form.save(commit=False)
            form.posted_by=recruiter
            form.save()
            return redirect('posted-jobs')
    else:
        form=JobPost
    return render(request,'job_form.html', {'form':form})


@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Recruiter'])
def updateJob(request,pk):
    job= JobPosition.objects.get(id=pk)
    form=JobPost(request.POST or None, instance=job)
    profile=Profile.objects.get(user=request.user)
    if job.posted_by.user!=profile.user:
        return HttpResponseForbidden('Sorry! You are not allowed to change this job!')
    if request.method=='POST':
        form=JobPost(request.POST or None, instance=job)
        if form.is_valid():
            form.save()
            return redirect('posted-jobs')
        
    return render(request,'job_form.html',{'form':form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def deleteJob(request, pk):
    job=JobPosition.objects.get(id=pk)
    job.delete()
    return redirect('posted-jobs')





@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def savedJobs(request):
    saved_jobs=SavedJobs.objects.filter(saver=request.user)
    jobs=Paginator(saved_jobs, 5)
    page=request.GET.get('page')
    items=jobs.get_page(page)
    return render(request, 'saved_jobs.html',{'saved_jobs': saved_jobs, 'items':items})



@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def saveJob(request, pk):
    job=JobPosition.objects.get(id=pk)
    saved=SavedJobs(
        saver=request.user,
        job=job,
    )
    
    try:
        SavedJobs.objects.get(job=job).job
        return HttpResponse('You have already saved this job! ')
    except:
        saved.save()
        return redirect('saved-jobs')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def unsaveJob(request, pk):
    job=SavedJobs.objects.get(id=pk)
    job.delete()
    return redirect('saved-jobs')


def home(request):
    if request.user.is_authenticated:
        if request.user.groups.all()[0].name=='Recruiter':
            return redirect('posted-jobs')
        else:
            return redirect('j-home')
    return render(request, 'home.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker', 'Recruiter'])
def jobListView(request):
   
    jobs=JobPosition.objects.all()
    p=Paginator(JobPosition.objects.all(), 5)
    page=request.GET.get('page')
    items=p.get_page(page)
    group=request.user.groups.all()[0].name
    context={
        'jobs': jobs,
        'items': items,
        "group": group,
    }
    return render(request, 'jobs.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker', 'Recruiter'])
def jobDetail(request,pk):
    job=JobPosition.objects.get(id=pk)
    group=request.user.groups.all()[0].name
    job_recruiter=job.posted_by.user
    context={
        'job':job,
        'group':group,
        'job_recruiter':job_recruiter,
    }
    return render(request, 'jobDetail.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker', 'Recruiter'])
def Contacts(request,pk):
    job=JobPosition.objects.get(id=pk)
    recruiter=job.posted_by
    context={
        'recruiter':recruiter,
    }
    return render(request,'contacts.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker', 'Recruiter'])
def searchJobs(request):
    search=''
    if request.method=='POST':
        
        search=request.POST['se']
        # jobs=JobPosition.objects.filter(title__icontains=search)
    p=Paginator(JobPosition.objects.filter(title__icontains=search), 5)
    page=request.GET.get('page')
    items=p.get_page(page)
       
    return render(request, 'searches.html', {'items':items,
                
                'search':search,
                })

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
def jobSeekerProfile(request):
    if request.method=='POST':
        form=JobSeekerProfile(request.POST or None)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=request.user
            form.save()
            return redirect('j-home')
    else:
        form=JobSeekerProfile()
    return render(request,'jobSeekerProfile.html', context={'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def jobSeekerEducation(request):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    if request.method=='POST':
        form=EducationForm(request.POST or None)
        if form.is_valid():
            education_experience = form.save(commit=False)
            education_experience.job_seeker = jobSeeker
            education_experience.save()
            return redirect('j-home')
    else:
        form=EducationForm()
    return render(request,'educationsF.html', context={'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def editEducation(request,pk):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    education=EducationExperience.objects.get(id=pk)
    form=EducationForm(request.POST or None, instance=education)
    if jobSeeker.user!=request.user:
        return HttpResponseForbidden('Sorry! You are not allowed to change this part!')
    if request.method=='POST':
        form=EducationForm(request.POST or None, instance=education)
        if form.is_valid():
            form.save()
            return redirect('educations')
        
    return render(request, 'educationsF.html', context={'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def educationsView(request):
    user=JobSeeker.objects.get(user=request.user)
    educations=EducationExperience.objects.filter(job_seeker=user)
    return render(request,'educationsView.html',{'educations':educations})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def educationsDelete(request, pk):
    educations=EducationExperience.objects.get(id=pk)
    educations.delete()
    return redirect('educations')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def jobSeekerWork(request):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    if request.method=='POST':
        form=JobExperienceForm(request.POST or None)
        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.job_seeker = jobSeeker
            work_experience.save()
            return redirect('j-home')
    else:
        form=JobExperienceForm()
    return render(request,'educationsF.html', context={'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def workView(request):
    user=JobSeeker.objects.get(user=request.user)
    jobs=JobExperience.objects.filter(job_seeker=user)
    return render(request,'workView.html',{'jobs':jobs})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def workDelete(request, pk):
    educations=JobExperience.objects.get(id=pk)
    educations.delete()
    return redirect('job-experiences')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def editWork(request,pk):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    job=JobExperience.objects.get(id=pk)
    form=JobExperienceForm(request.POST or None, instance=job)
    if jobSeeker.user!=request.user:
        return HttpResponseForbidden('Sorry! You are not allowed to change this part!')
    if request.method=='POST':
        form=JobExperienceForm(request.POST or None, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job-experiences')
        
    return render(request, 'educationsF.html', context={'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def jobSeekerSkill(request):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    if request.method=='POST':
        form=SkillForm(request.POST or None)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.job_seeker = jobSeeker
            skill.save()
            return redirect('j-home')
    else:
        form=SkillForm()
    return render(request,'educationsF.html', context={'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def skillView(request):
    user=JobSeeker.objects.get(user=request.user)
    skills=Skill.objects.filter(job_seeker=user)
    return render(request,'skillView.html',{'skills':skills})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def skillDelete(request, pk):
    skill=Skill.objects.get(id=pk)
    skill.delete()
    return redirect('skills')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def editSkill(request,pk):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    skill=Skill.objects.get(id=pk)
    form=SkillForm(request.POST or None, instance=skill)
    if jobSeeker.user!=request.user:
        return HttpResponseForbidden('Sorry! You are not allowed to change this part!')
    if request.method=='POST':
        form=SkillForm(request.POST or None, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skills')
        
    return render(request, 'educationsF.html', context={'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def resumeView(request):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    jobExperiences=JobExperience.objects.filter(job_seeker=jobSeeker)
    educations=EducationExperience.objects.filter(job_seeker=jobSeeker)
    skills=Skill.objects.filter(job_seeker=jobSeeker)
    context={
        'job_seeker': jobSeeker,
        'job_experiences':jobExperiences,
        'education_experiences':educations,
        'skills':skills,
    }
    return render(request,'resume.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Job_Seeker'])
@profileMaking
def jobSeekerHomePage(request):
    return render(request, 'jobSeekerHome.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Job_Seeker'])
@profileMaking
def updateJobSeekerProfile(request):
    jobSeeker= JobSeeker.objects.get(user=request.user)
    form=JobSeekerProfile(request.POST or None, instance=jobSeeker)
    if request.method=='POST':
        form=JobSeekerProfile(request.POST or None, instance=jobSeeker)
        if form.is_valid():
            form.save()
            return redirect('j-home')
        
    return render(request,'jobSeekerProfile.html',{'form':form, 'jobSeeker':jobSeeker})

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Job_Seeker'])
@profileMaking
def applyJob(request, pk):
    try:
        jobSeeker= JobSeeker.objects.get(user=request.user)
        job=JobPosition.objects.get(id=pk)
        try:
            if job.applied_persons.get(user=request.user):
                return HttpResponse('Sorry! You have alredy applied for this!')
        except:
            pass
    except:
        return HttpResponse('Job seeker not found!!!')
    job=JobPosition.objects.get(id=pk)
    job.applied_persons.add(jobSeeker)
    job.save()
    return redirect('jobs')

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Job_Seeker'])
@profileMaking
def unapplyJob(request, pk):
    try:
        jobSeeker= JobSeeker.objects.get(user=request.user)
    except:
        return HttpResponse('Job seeker not found!!!')
    job=JobPosition.objects.get(id=pk)
    job.applied_persons.remove(jobSeeker) # remove the job seeker object
    return redirect('applied-jobs')

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Job_Seeker'])
@profileMaking
def appliedJobs(request):
    jobSeeker=JobSeeker.objects.get(user=request.user)
    try:
        jobs=JobPosition.objects.filter(applied_persons=jobSeeker)
        p=Paginator(jobs, 5)
        page=request.GET.get('page')
        items=p.get_page(page)
    except:
        return  HttpResponse('Sorry! Something went wrong!!!')

    return render(request,'applied.html',{'items':items})


@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Recruiter'])
def appliedJobSeekers(request, pk):
    job=JobPosition.objects.get(id=pk)
    applied=job.applied_persons
    return render(request,'appliedJobSeekers.html', {'job':job, 'applied':applied})

@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'Recruiter'])
def jobSeekerResumeView(request,pk):
    jobSeeker=JobSeeker.objects.get(id=pk)
    jobExperiences = JobExperience.objects.filter(job_seeker=jobSeeker)
    educations = EducationExperience.objects.filter(job_seeker=jobSeeker)
    skills = Skill.objects.filter(job_seeker=jobSeeker)
    context = {
        'job_seeker': jobSeeker,
        'job_experiences': jobExperiences,
        'education_experiences': educations,
        'skills': skills,
    }
    return render(request,'resume.html', context)

