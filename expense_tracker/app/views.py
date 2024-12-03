import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password #hash the password
from django.core.paginator import Paginator
from django.db.models import Avg, Sum
from .forms import UserForm, UserProfileForm, LoginForm, AddMoneyForm
from .models import UserProfile, AddMoneyInfo

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
            money_type = expenses_form.cleaned_data["money_type"]
            quantity = expenses_form.cleaned_data["quantity"]

            expense = expenses_form.save(commit=False)
            expense.user = request.user
            expense.save()

            user_profile = UserProfile.objects.get(user=request.user)

            if money_type == "Expense":
                user_profile.expenses = user_profile.expenses + quantity
                user_profile.save(update_fields=["expenses"])
            elif money_type == "Saving":
                user_profile.savings = user_profile.savings + quantity
                user_profile.save(update_fields=["savings"])
            elif money_type == "Income":
                user_profile.income = user_profile.income + quantity
                user_profile.save(update_fields=["income"])

            return redirect("/home")
    else:
        expenses_form = AddMoneyForm()

    return render(request, 'add_expenses.html', {"expenses_form": expenses_form})

def history(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")

    user_addings = AddMoneyInfo.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(user_addings, 7)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "history.html", {"page_obj": page_obj})

def thirty_days_expense(request):
    today = datetime.date.today()
    one_month_ago = today - datetime.timedelta(days=30)

    current_user = request.user

    if not current_user.is_authenticated:
        return render(request, "index.html")

    money_info_queryset = AddMoneyInfo.objects.filter(user=current_user, money_type="Expense", date__gte=one_month_ago, date__lte=today)
    print("QUERY SET = ", money_info_queryset)
    expense_summary = get_expense_category(money_info_queryset)

    return render(request, "thirty_days.html", {"expense_summary": expense_summary})

def get_expense_category(money_info_queryset):
    expense_categories = money_info_queryset.filter(
        money_type="Expense").values_list("category", flat=True).distinct()

    final_report = {}
    for category in expense_categories:
        total_quantity = money_info_queryset.filter(
            category=category, money_type="Expense").aggregate(total=Sum("quantity"))['total']
        final_report[category] = total_quantity or 0

    return final_report


def delete_expense(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")


    try:
        if request.method == "POST":
            expense_adding_id = request.POST.get("expense_id")
            expense_adding = AddMoneyInfo.objects.get(user=request.user, id=expense_adding_id)
            user_profile = UserProfile.objects.get(user=request.user)

            if expense_adding.money_type == "Expense":
                user_profile.expenses = user_profile.expenses - expense_adding.quantity
                user_profile.save(update_fields=["expenses"])
            elif expense_adding.money_type == "Saving":
                user_profile.savings = user_profile.savings - expense_adding.quantity
                user_profile.save(update_fields=["savings"])
            elif expense_adding.money_type == "Income":
                user_profile.income = user_profile.income - expense_adding.quantity
                user_profile.save(update_fields=["income"])

            expense_adding.delete()

            return redirect("/history")
    except AddMoneyInfo.DoesNotExist:
        return render(request, "history.html", {"error": "Entry doesn't exist"})


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
