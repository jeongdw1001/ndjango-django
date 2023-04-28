from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import redirect
from .models import CustomUser
from django.http import HttpResponse
from .forms import RegistrationForm, CustomUserChangeForm

# Create your views here.

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            print("로그인 성공")
            login(request, user)
            return redirect('users:login')
        else:
            print("로그인 실패")
            return HttpResponse('로그인 실패')
    context = {}
    
    return render(request, "users/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("users:login")

def signup_view(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegistrationForm()
    return render(request, "users/signup.html", {'form': form})


def update_view(request):

    if request.method == "POST":
        editForm = CustomUserChangeForm(request.POST, instance=request.user)
        if editForm.is_valid():
            editForm.save()
            return redirect('homepage:index')
    else:
        editForm = CustomUserChangeForm(instance=request.user)

    return render(request, "users/update.html", {'editForm': editForm})
    

