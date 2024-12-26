import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password #hash the password
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Sum
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
    current_balance = user_profile.income - user_profile.expenses

    today = datetime.date.today()
    month = today.month
    year = today.year
    month_name = today.strftime("%B")

    this_month_expenses = AddMoneyInfo.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year,
        money_type="Expense"
    ).aggregate(total=Sum("quantity"))

    this_month_income = AddMoneyInfo.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year,
        money_type="Income"
    ).aggregate(total=Sum("quantity"))

    this_month_savings = AddMoneyInfo.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year,
        money_type="Saving"
    ).aggregate(total=Sum("quantity"))

    context = {
        "user": request.user, 
        "savings": user_profile.savings, 
        "current_balance": current_balance,
        "this_month_expenses": this_month_expenses['total'],
        "this_month_income": this_month_income['total'],
        "this_month_savings": this_month_savings['total'],
        "month": month_name, 
        "year": year,
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

def update_profile(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")

    if request.method == "POST":
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            return HttpResponse("Profile does not exist, please create one.", status=404)

        profile_form = UserProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect("/home")
    else:
        profile_form = UserProfileForm()

        return render(request, "update_profile.html", {"profile_form": profile_form})

def update_entry(request):
    pass

def history(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")

    user_addings = AddMoneyInfo.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(user_addings, 7)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "history.html", {"page_obj": page_obj})

def year_to_date_summary(request):
    today_lte = datetime.date.today()
    year_ago_gte = today_lte - datetime.timedelta(days=365)

    current_user = request.user

    if not current_user.is_authenticated:
        return render(request, "index.html")

    expense_summary = get_summary(current_user, "Expense", today_lte, year_ago_gte)
    income_summary = get_summary(current_user, "Income", today_lte, year_ago_gte)
    saving_summary = get_summary(current_user, "Saving", today_lte, year_ago_gte)

    context = {
        "expense_summary": expense_summary,
        "income_summary": income_summary, 
        "saving_summary": saving_summary,
        "title": "Last 356 Days",
    }

    return render(request, "summary.html", context)

def thirty_days_summary(request):
    today_lte = datetime.date.today()
    month_ago_gte = today_lte - datetime.timedelta(days=30)

    current_user = request.user

    if not current_user.is_authenticated:
        return render(request, "index.html")

    expense_summary = get_summary(current_user, "Expense", today_lte, month_ago_gte)
    income_summary = get_summary(current_user, "Income", today_lte, month_ago_gte)
    saving_summary = get_summary(current_user, "Saving", today_lte, month_ago_gte)

    context = {
        "expense_summary": expense_summary,
        "income_summary": income_summary, 
        "saving_summary": saving_summary,
        "title": "Last 30 Days"
    }

    return render(request, "summary.html",  context)

def one_week_summary(request):
    today_lte = datetime.date.today()
    week_ago_gte = today_lte - datetime.timedelta(days=7)

    current_user = request.user
    if not current_user.is_authenticated:
        return render(request, "index.html")

    expense_summary = get_summary(current_user, "Expense", today_lte, week_ago_gte)
    income_summary = get_summary(current_user, "Income", today_lte, week_ago_gte)
    saving_summary = get_summary(current_user, "Saving", today_lte, week_ago_gte)

    context = {
        "expense_summary": expense_summary,
        "income_summary": income_summary, 
        "saving_summary": saving_summary,
        "title": "1 week summary"
    }

    return render(request, "summary.html",  context)


def get_summary(current_user, money_type, today_lte, ago_gte):
    queryset = AddMoneyInfo.objects.filter(user=current_user, money_type=money_type, date__gte=ago_gte, date__lte=today_lte)

    def get_total(queryset, money_type):
        if money_type == "Expense":
            expense_categories = queryset.filter(
                money_type=money_type).values_list("category", flat=True).distinct()

            final_report = {}
            for category in expense_categories:
                total_quantity = queryset.filter(
                    category=category, money_type=money_type).aggregate(total=Sum("quantity"))['total']
                final_report[category] = total_quantity or 0

            final_report["Total"] = queryset.filter(money_type=money_type).aggregate(total=Sum("quantity"))['total']
            return final_report
        else:
            total_quantity = queryset.filter(money_type=money_type).aggregate(total=Sum("quantity"))['total']
            return total_quantity

    summary = get_total(queryset, money_type)
    return summary


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
