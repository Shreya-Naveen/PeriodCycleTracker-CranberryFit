from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MenstrualTracking, SymptomTracking, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'phone_number', 'emergency_contact']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MenstrualTrackingForm(forms.ModelForm):
    class Meta:
        model = MenstrualTracking
        fields = ['cycle_length', 'last_period_start']
        widgets = {
            'last_period_start': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'cycle_length': 'Cycle Length (in days)',
            'last_period_start': 'Last Period Start Date',
        }

class SymptomTrackingForm(forms.ModelForm):
    class Meta:
        model = SymptomTracking
        fields = ['cramps', 'mood', 'trained_today', 'performance_rating']
        widgets = {
            'performance_rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'cramps': 'Cramps',
            'mood': 'Mood',
            'trained_today': 'Did you train today?',
            'performance_rating': 'Performance Rating (1-10)',
        }
