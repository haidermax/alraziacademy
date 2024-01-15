from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import UserProfile
from course.models import *
def index(request):
    success_messages = messages.get_messages(request)
    depts= Speciality.objects.all()
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    else:
        user_profile=None
    user = request.user
    context={'user':user,'profile':user_profile, 'dept':depts}
    return render(request,"index.html",context)


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request,'dashboard.html')
        else:
            return redirect('index')
    return redirect('index')