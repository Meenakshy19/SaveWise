from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from .models import Income,Expense,Budget,Goal,Savings
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not name or not email or not password or not confirm_password:
            messages.error(request, "Please fill in all fields!")

        elif User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists!")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match!")

        else:
            User.objects.create_user(
                username=email,
                first_name=name,
                email=email,
                password=password
            )
            messages.success(request, "Account created successfully!")

    return render(request, 'core/signup.html')
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password!")

    return render(request, 'core/login.html')
@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    savings = Savings.objects.filter(user=request.user)
    goals = Goal.objects.filter(user=request.user)

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    total_savings = sum(saving.amount for saving in savings)

    if total_expense <= total_income:
        remaining_income = total_income - total_expense
        remaining_savings = total_savings
    else:
        remaining_expense = total_expense - total_income
        remaining_income = 0
        remaining_savings = total_savings - remaining_expense

    total_balance = remaining_income + remaining_savings

    for goal in goals:
        goal.progress = (goal.saved_amount / goal.target_amount) * 100

    return render(request, 'core/dashboard.html', {
        'incomes': incomes,
        'expenses': expenses,
        'goals': goals,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_balance': total_balance,
        'total_savings': total_savings,
        'remaining_income': remaining_income,
        'remaining_savings': remaining_savings
    })
@login_required
def reports(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    savings = Savings.objects.filter(user=request.user)

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    total_savings = sum(saving.amount for saving in savings)

    if total_expense <= total_income:
        remaining_income = total_income - total_expense
        remaining_savings = total_savings
    else:
        remaining_expense = total_expense - total_income
        remaining_income = 0
        remaining_savings = total_savings - remaining_expense

    total_balance = remaining_income + remaining_savings

    categories = {}

    for expense in expenses:
        if expense.category in categories:
            categories[expense.category] += expense.amount
        else:
            categories[expense.category] = expense.amount

    return render(request, 'core/reports.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'total_savings': total_savings,
        'remaining_income': remaining_income,
        'remaining_savings': remaining_savings,
        'total_balance': total_balance,
        'categories': categories
    })
@login_required   
def income(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        amount = request.POST.get('amount')

        if source and amount:
            Income.objects.create(
                user=request.user,
                source=source,
                amount=amount
            )

            messages.success(request, "Income added successfully!")

    return render(request, 'core/income.html')
@login_required
def expense(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        amount = request.POST.get('amount')

        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount
        )

        messages.success(request, "Expense added successfully!")

    return render(request, 'core/expense.html')
@login_required
def budget(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        month = request.POST.get('month')

        Budget.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            month=month
        )
        
        messages.success(request, "Budget set successfully!")

    budgets = Budget.objects.filter(user=request.user) 

    for budget in budgets:
        budget.spent = sum(
            expense.amount
            for expense in Expense.objects.filter(
                user=request.user,
                category=budget.category
            )
        )  
        budget.remaining = budget.amount - budget.spent

        if budget.spent > budget.amount:
            budget.exceeded = True
        else:
            budget.exceeded = False

    return render(request, 'core/budget.html',{
        'budgets': budgets
    })
@login_required
def goal(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        target_amount = request.POST.get('target_amount')
        target_date = request.POST.get('target_date')
        saved_amount = request.POST.get('saved_amount')

        Goal.objects.create(
            user=request.user,
            name=name,
            target_amount=target_amount,
            target_date=target_date,
            saved_amount=saved_amount,
        )

        messages.success(request, "Goal created successfully!")

    return render(request, 'core/goal.html')
@login_required
def savings(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        if amount:
            Savings.objects.create(
                user=request.user,
                amount=amount
            )

            messages.success(request, "Savings added successfully!")

    return render(request, 'core/savings.html')
@login_required
def delete_goal(request, id):
    goal = Goal.objects.get(id=id, user=request.user)
    goal.delete()
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')