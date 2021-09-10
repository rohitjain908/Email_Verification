from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from accounts.forms import Userform
from django.contrib.auth.models import User
from .models import Profile
import uuid ##for creating unique token for each user
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def home(request):
  return render(request,'accounts/home.html')


def index(request):
  if request.user.is_authenticated:
    return render(request,'accounts/user.html')
  else:
    return redirect('login_view')


  
def login_view(request):
  if request.user.is_authenticated:
    return render(request,'accounts/user.html')
  else:
    if request.method=="POST":
      username=request.POST['username']
      password=request.POST['password']

      user_obj=authenticate(request,username=username,password=password)

      if user_obj is not None:
        profile_obj=Profile.objects.filter(user=user_obj).first()
        if profile_obj.is_varified:
          login(request,user_obj)
          return render(request,'accounts/user.html',{'request':request})
        else:
          messages.success(request,'*Your account is not verified yet')
          return render(request,'accounts/login.html')

      else:
        messages.success(request,'*Invalid Credantial')
        return render(request,'accounts/login.html')

    return render(request,'accounts/login.html')  

def register(request):
  if request.user.is_authenticated:
    return render(request,'accounts/user.html')
  else:
    if request.method=="POST":
      form=Userform(request.POST)
      if form.is_valid():
        form.save()  ##information is valid so user is created and now we can access it from User model

        user_obj=User.objects.filter(username=request.POST['username']).first()
        auth_token=str(uuid.uuid4())
        print(auth_token)
        profile_obj=Profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        #print(user_obj.email)
        send_mail_after_registration(user_obj.email,auth_token)
        return redirect("token")
      else:
        return render(request,'accounts/register.html',{"form":form})
    form=Userform()
    return render(request,'accounts/register.html',{"form":form})

def logout_view(request):
  logout(request)
  return redirect("login_view")


def token(request):
  return render(request,'accounts/token.html')

def verify(request,auth_token):
  #print(auth_token)
  profile_obj=Profile.objects.filter(auth_token=auth_token).first()
  if profile_obj:
    if profile_obj.is_varified:
      messages.success(request,'Your account is already verified')
      return render(request,'accounts/verify.html')
    messages.success(request,'Your account is successfully verified')
    profile_obj.is_varified=True
    profile_obj.save()
    #print(profile_obj.is_varified)
    return render(request,'accounts/verify.html')
  else:
    return redirect('error')

def error_page(request):
  return render(request,'accounts/error.html')


def send_mail_after_registration(email , token):
  subject = 'Your accounts need to be verified'
  message = f'Hi paste the link to verify your account http://127.0.0.1:8000/accounts/verify/{token}'
  email_from = settings.EMAIL_HOST_USER
  recipient_list = [email]
  send_mail(subject, message , email_from ,recipient_list )
    

