from django import forms
from django.contrib.auth.models import User
from common.djangoapps.student.models import UserProfile
from .models import Franchise

class SimpleUserRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30, label="Full Name", required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    franchise = forms.ModelChoiceField(
        queryset=Franchise.objects.all(),
        required=False,
        label="Select Franchise"
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        name_parts = self.cleaned_data['full_name'].split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'name': self.cleaned_data['full_name']}
            )
        return user

class FranchiseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ['name', 'location', 'joining_date']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'})
        }