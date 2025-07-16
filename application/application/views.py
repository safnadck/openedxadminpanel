from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from common.djangoapps.student.models import UserProfile
from .forms import SimpleUserRegistrationForm, FranchiseRegistrationForm
from .models import Franchise, UserFranchise

@login_required
def user_and_franchise_management(request):
    if request.method == 'POST':
        if 'user_form_submit' in request.POST:
            user_form = SimpleUserRegistrationForm(request.POST)
            franchise_form = FranchiseRegistrationForm()
            if user_form.is_valid():
                user = user_form.save()
                franchise = user_form.cleaned_data.get('franchise')
                if franchise:
                    UserFranchise.objects.create(user=user, franchise=franchise)
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

    users = []
    for user in User.objects.all():
        try:
            user_franchise = UserFranchise.objects.get(user=user)
            franchise_name = user_franchise.franchise.name
        except UserFranchise.DoesNotExist:
            franchise_name = "No Franchise"
        
        try:
            profile = UserProfile.objects.get(user=user)
            full_name = profile.name
        except UserProfile.DoesNotExist:
            full_name = f"{user.first_name} {user.last_name}".strip()

        users.append({
            'id': user.id,
            'username': user.username,
            'first_name': full_name,
            'email': user.email,
            'franchises': franchise_name
        })

    franchises = Franchise.objects.all()
    
    return render(request, 'application/user_and_franchise_management.html', {
        'users': users,
        'franchises': franchises,
        'user_form': user_form,
        'franchise_form': franchise_form
    })