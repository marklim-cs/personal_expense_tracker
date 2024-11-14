from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password #hash the password
from .forms import UserForm, UserProfileForm, LoginForm
from .models import UserProfile

def index(request):
    if request.user.is_authenticated:
        return redirect("/home")
    else:
        return render(request, "index.html")

def home(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")

    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        "user": request.user, 
        "profession": user_profile.profession, 
        "savings": user_profile.savings, 
        "income": user_profile.income,
    }

    return render(request, "home.html", context)

def handle_signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.password = make_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)

            return redirect('/home')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "signup.html", {'user_form': user_form, 'profile_form': profile_form})

def handle_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home")
            else:
                messages.error(request, "Invalid username or password. Please, try again.")
                return render(request, "login.html", {"login_form": login_form})

    else:
        login_form = LoginForm()

    return render(request, "login.html", {"login_form": login_form})

def handle_logout(request):
    logout(request)
    messages.success(request, "Successfuly logged out!")
    return render(request, "logout.html")