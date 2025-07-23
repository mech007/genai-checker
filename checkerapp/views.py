from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, MakerFormEntryForm
from .models import Profile, MakerFormEntry  # <-- import Profile and MakerFormEntry here

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, role=form.cleaned_data['role'])  # now this works
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    profile = request.user.profile
    if profile.role == 'maker':
        forms = MakerFormEntry.objects.filter(maker=request.user)
        return render(request, 'maker_dashboard.html', {'forms': forms})
    elif profile.role == 'checker':
        forms = MakerFormEntry.objects.all()
        return render(request, 'checker_dashboard.html', {'forms': forms})
    return redirect('login')

@login_required
def submit_form_view(request):
    if request.user.profile.role != 'maker':
        return redirect('dashboard')
    if request.method == 'POST':
        form = MakerFormEntryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.maker = request.user
            instance.save()
            return redirect('dashboard')
    else:
        form = MakerFormEntryForm()
    return render(request, 'maker_form.html', {'form': form})

@login_required
def edit_form_view(request, form_id):
    if request.user.profile.role != 'checker':
        return redirect('dashboard')
    form_entry = MakerFormEntry.objects.get(id=form_id)
    if request.method == 'POST':
        decision = request.POST.get('decision')
        form_entry.ai_decision = decision
        form_entry.save()
        return redirect('dashboard')
    return render(request, 'edit_form.html', {'form_entry': form_entry})

def logout_view(request):
    logout(request)
    return redirect('login')