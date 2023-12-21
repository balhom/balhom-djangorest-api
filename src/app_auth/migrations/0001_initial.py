# Generated by Django 4.2.8 on 2023-12-21 07:10

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import src.app_auth.models.user_model
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('keycloak_id', models.TextField(editable=False, unique=True, verbose_name='keycloak id')),
                ('image', models.ImageField(default='users/default_user.jpg', upload_to=src.app_auth.models.user_model._image_user_dir, verbose_name='profile image')),
                ('current_balance', models.FloatField(default=0.0, verbose_name='current balance')),
                ('receive_email_balance', models.BooleanField(default=True, verbose_name='receive email about balance')),
                ('expected_annual_balance', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='expected annual balance')),
                ('expected_monthly_balance', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='expected monthly balance')),
                ('date_pass_reset', models.DateTimeField(blank=True, null=True, verbose_name='date of last password reset code sent')),
                ('count_pass_reset', models.IntegerField(default=0, verbose_name='number of requests for password reset')),
                ('pref_currency_type', models.CharField(max_length=4, verbose_name='preferred currency type')),
                ('date_currency_change', models.DateTimeField(blank=True, null=True, verbose_name='date of last preferred currency type change')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', src.app_auth.models.user_model.BalanceUserManager()),
            ],
        ),
    ]