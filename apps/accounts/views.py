from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProfileUpdateForm


# Create your views here.
def home(request):
    # Exclude the admin account (e.g., "pritangshu") from the user list
    users = User.objects.exclude(username="pritangshu")
    return render(request, "accounts/accounts.html", {"users": users})

def about(request):
    return render(request, 'about.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username'].lower()  # Convert to lowercase
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username'].lower()  # Convert to lowercase
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('register')
            user = User.objects.create_user(
                username=username,
                password=password
            )
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'accounts/register.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def searched(request):
    query = request.GET.get('query')
    users = User.objects.filter(username__icontains = query)
    return render(request, "accounts/accounts.html",  {"users": users})

def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("register")  # Redirect to the registration page after deletion
    return render(request, "accounts/delete_account.html")

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/update_profile.html', {'form': form})