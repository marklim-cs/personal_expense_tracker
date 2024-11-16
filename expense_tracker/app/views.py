from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password #hash the password
from .forms import UserForm, UserProfileForm, LoginForm, AddMoneyForm
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
        "expenses": user_profile.expenses,
    }

    return render(request, "home.html", context)

def add_expenses(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")

    if request.method == "POST":
        expenses_form = AddMoneyForm(request.POST)

        if expenses_form.is_valid():
            expense_type = expenses_form.cleaned_data["expense_type"]
            quantity = expenses_form.cleaned_data["quantity"]

            expense = expenses_form.save(commit=False)
            expense.user = request.user
            expense.save()

            user_profile = UserProfile.objects.get(user=request.user)

            if expense_type == "Expense":
                user_profile.expenses = user_profile.expenses + quantity
                user_profile.save(update_fields=["expenses"])
            elif expense_type == "Saving":
                user_profile.savings = user_profile.savings + quantity
                user_profile.save(update_fields=["savings"])
            elif expense_type == "Income":
                user_profile.income = user_profile.income + quantity
                user_profile.save(update_fields=["income"])

            return redirect("/home")
    else:
        expenses_form = AddMoneyForm()

    return render(request, 'add_expenses.html', {"expenses_form": expenses_form})

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