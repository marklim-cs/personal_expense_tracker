from django.shortcuts import render, HttpResponseRedirect
#from django.contrib.auth import authenticate
#from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password #hash the password
from .forms import UserForm, UserProfileForm


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

            return HttpResponseRedirect('/registered/')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "signup.html", {'user_form': user_form, 'profile_form': profile_form})
