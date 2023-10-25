from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import JobPosition, Profile
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import authenticatedUser, allowed_users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group 
from .forms import ContactForm, JobPost

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
                return redirect('jobs')
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
            return redirect('jobs')
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




def home(request):
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