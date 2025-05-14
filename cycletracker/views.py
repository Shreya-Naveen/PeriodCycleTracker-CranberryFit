from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.db.models import Avg, StdDev
from datetime import datetime, timedelta
from .forms import (
    MenstrualTrackingForm, SymptomTrackingForm,
    CustomUserCreationForm, UserProfileForm
)
from .models import MenstrualTracking, SymptomTracking

class CustomLoginView(LoginView):
    template_name = 'cycletracker/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have been successfully logged in!')
        return response

def login_view(request):
    return CustomLoginView.as_view()(request)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out!')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create the user
            user = user_form.save()
            
            # Update the user's profile with the additional information
            profile = user.userprofile  # This will exist due to the signal
            profile.birth_date = profile_form.cleaned_data.get('birth_date')
            profile.phone_number = profile_form.cleaned_data.get('phone_number')
            profile.emergency_contact = profile_form.cleaned_data.get('emergency_contact')
            profile.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'cycletracker/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def home(request):
    next_period_date = None
    days_until_period = None
    cycle_progress = None
    average_cycle_length = None
    cycle_variation = None
    last_period_start = None

    # Get user's cycle data
    menstrual_entries = MenstrualTracking.objects.filter(user=request.user).order_by('-submission_date')
    
    if menstrual_entries.exists():
        # Calculate average cycle length and variation
        cycle_stats = menstrual_entries.aggregate(
            avg_length=Avg('cycle_length'),
            std_dev=StdDev('cycle_length')
        )
        average_cycle_length = round(cycle_stats['avg_length'] or 0)
        cycle_variation = round(cycle_stats['std_dev'] or 0)

        # Get the most recent entry
        latest_entry = menstrual_entries.first()
        last_period_start = latest_entry.last_period_start

        # Calculate next period date
        next_period_date = last_period_start + timedelta(days=latest_entry.cycle_length)
        
        # Calculate days until next period
        today = datetime.now().date()
        days_until_period = (next_period_date - today).days
        
        # Calculate cycle progress
        days_since_last_period = (today - last_period_start).days
        cycle_progress = min(100, max(0, int((days_since_last_period / latest_entry.cycle_length) * 100)))

    if request.method == 'POST':
        menstrual_form = MenstrualTrackingForm(request.POST)
        symptom_form = SymptomTrackingForm(request.POST)

        if menstrual_form.is_valid() and symptom_form.is_valid():
            # Save menstrual tracking data
            menstrual_data = menstrual_form.save(commit=False)
            menstrual_data.user = request.user
            menstrual_data.save()
            
            # Save symptom tracking data
            symptom_data = symptom_form.save(commit=False)
            symptom_data.user = request.user
            symptom_data.tracking_date = menstrual_data.last_period_start
            symptom_data.save()

            messages.success(request, 'Your data has been successfully saved!')
            return redirect('home')
    else:
        menstrual_form = MenstrualTrackingForm()
        symptom_form = SymptomTrackingForm()

    # Get recent entries for display
    recent_entries = menstrual_entries[:5]
    recent_symptoms = SymptomTracking.objects.filter(user=request.user).order_by('-tracking_date')[:5]

    return render(request, 'cycletracker/home.html', {
        'menstrual_form': menstrual_form,
        'symptom_form': symptom_form,
        'next_period_date': next_period_date,
        'days_until_period': days_until_period,
        'cycle_progress': cycle_progress,
        'average_cycle_length': average_cycle_length,
        'cycle_variation': cycle_variation,
        'last_period_start': last_period_start,
        'recent_entries': recent_entries,
        'recent_symptoms': recent_symptoms,
    })

@login_required
def history(request):
    menstrual_entries = MenstrualTracking.objects.filter(user=request.user).order_by('-submission_date')
    symptom_entries = SymptomTracking.objects.filter(user=request.user).order_by('-tracking_date')
    
    return render(request, 'cycletracker/history.html', {
        'menstrual_entries': menstrual_entries,
        'symptom_entries': symptom_entries,
    })

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'cycletracker/profile.html', {
        'profile_form': profile_form
    })

def information(request):
    """View for the information page about menstrual health."""
    current_phase = None
    phase_info = None
    days_in_cycle = None
    
    if request.user.is_authenticated:
        # Get user's cycle data
        menstrual_entries = MenstrualTracking.objects.filter(user=request.user).order_by('-submission_date')
        
        if menstrual_entries.exists():
            latest_entry = menstrual_entries.first()
            cycle_length = latest_entry.cycle_length
            last_period_start = latest_entry.last_period_start
            today = datetime.now().date()
            
            # Calculate days since last period
            days_in_cycle = (today - last_period_start).days
            
            # Calculate phase based on cycle length
            if days_in_cycle <= 5:  # Menstrual Phase
                current_phase = "Menstrual"
                phase_info = {
                    "description": "You are in your menstrual phase. This is when your period occurs.",
                    "suggestions": [
                        "Focus on gentle exercises like yoga or walking",
                        "Stay hydrated and maintain iron-rich foods",
                        "Get plenty of rest",
                        "Use heat therapy for cramps",
                        "Practice stress-reduction techniques"
                    ]
                }
            elif days_in_cycle <= (cycle_length * 0.4):  # Follicular Phase
                current_phase = "Follicular"
                phase_info = {
                    "description": "You are in your follicular phase. Your body is preparing for ovulation.",
                    "suggestions": [
                        "Great time for strength training and HIIT workouts",
                        "Focus on protein-rich foods",
                        "Take advantage of increased energy levels",
                        "Plan challenging workouts",
                        "Stay hydrated and maintain electrolyte balance"
                    ]
                }
            elif days_in_cycle <= (cycle_length * 0.6):  # Ovulation Phase
                current_phase = "Ovulation"
                phase_info = {
                    "description": "You are in your ovulation phase. This is when an egg is released.",
                    "suggestions": [
                        "Moderate intensity workouts are ideal",
                        "Focus on balanced nutrition",
                        "Stay hydrated",
                        "Listen to your body's energy levels",
                        "Maintain consistent exercise routine"
                    ]
                }
            else:  # Luteal Phase
                current_phase = "Luteal"
                phase_info = {
                    "description": "You are in your luteal phase. Your body is preparing for the next cycle.",
                    "suggestions": [
                        "Focus on endurance and flexibility exercises",
                        "Include complex carbohydrates in your diet",
                        "Practice stress management",
                        "Get adequate sleep",
                        "Stay hydrated and watch for bloating"
                    ]
                }
    
    return render(request, 'cycletracker/information.html', {
        'current_phase': current_phase,
        'phase_info': phase_info,
        'days_in_cycle': days_in_cycle
    })
