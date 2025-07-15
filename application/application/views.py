from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SimpleUserRegistrationForm, FranchiseRegistrationForm
from .models import Franchise

@login_required
def user_and_franchise_management(request):
    if request.method == 'POST':
        if 'user_form_submit' in request.POST:
            user_form = SimpleUserRegistrationForm(request.POST)
            franchise_form = FranchiseRegistrationForm()
            if user_form.is_valid():
                user_form.save()
                return redirect('application:user_and_franchise_management')

        elif 'franchise_form_submit' in request.POST:
            franchise_form = FranchiseRegistrationForm(request.POST)
            user_form = SimpleUserRegistrationForm()
            if franchise_form.is_valid():
                franchise_form.save()
                return redirect('application:user_and_franchise_management')
    else:
        user_form = SimpleUserRegistrationForm()
        franchise_form = FranchiseRegistrationForm()

    users = User.objects.all().values('id', 'username', 'first_name', 'email')
    franchises = Franchise.objects.all().values('id', 'name', 'location', 'joining_date')

    return render(request, 'application/user_and_franchise_management.html', {
        'users': users,
        'franchises': franchises,
        'user_form': user_form,
        'franchise_form': franchise_form
    })
