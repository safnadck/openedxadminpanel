from django import forms
from django.contrib.auth.models import User
from common.djangoapps.student.models import UserProfile
from .models import Franchise

class SimpleUserRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30, label="Full Name", required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user)

        return user

class FranchiseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ['name', 'location', 'joining_date']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'})
        }
