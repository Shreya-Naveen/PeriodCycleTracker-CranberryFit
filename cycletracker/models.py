from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class MenstrualTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cycle_length = models.IntegerField()
    last_period_start = models.DateField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'}'s Cycle: {self.cycle_length} days, Last Period: {self.last_period_start}"

class SymptomTracking(models.Model):
    CRAMP_CHOICES = [
        ('None', 'None'),
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe')
    ]
    
    MOOD_CHOICES = [
        ('Happy', 'Happy'),
        ('Neutral', 'Neutral'),
        ('Irritable', 'Irritable'),
        ('Anxious', 'Anxious'),
        ('Sad', 'Sad')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tracking_date = models.DateField(auto_now_add=True)
    cramps = models.CharField(max_length=10, choices=CRAMP_CHOICES)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    trained_today = models.BooleanField()
    performance_rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'}'s Symptoms: {self.tracking_date}: {self.cramps}, {self.mood}"
