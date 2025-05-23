# Generated by Django 5.1.5 on 2025-01-31 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenstrualTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle_length', models.IntegerField()),
                ('last_period_start', models.DateField()),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SymptomTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_date', models.DateField(auto_now_add=True)),
                ('cramps', models.CharField(choices=[('None', 'None'), ('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')], max_length=10)),
                ('mood', models.CharField(choices=[('Happy', 'Happy'), ('Neutral', 'Neutral'), ('Irritable', 'Irritable'), ('Anxious', 'Anxious'), ('Sad', 'Sad')], max_length=10)),
                ('trained_today', models.BooleanField()),
                ('performance_rating', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
