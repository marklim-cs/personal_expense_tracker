from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password #hash the password
from .forms import UserForm, UserProfileForm, LoginForm


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

            return redirect('/success')
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
                request.session['logged_in'] = True
                user_id = request.user.id
                request.session['user_ud'] = user_id
                messages.success(request, " Successfuly logged in!")

                return redirect("/success")
            else:
                messages.error(request, " Invalid Credentials. Please try again")
                return redirect("/login")

    else:
        login_form = LoginForm()

    return render(request, "login.html", {"login_form": login_form})