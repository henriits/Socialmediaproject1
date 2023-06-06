# Generated by Django 4.2.1 on 2023-06-06 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key='True', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.ImageField(default='default_profile_pic.png', upload_to='profile_pics')),
                ('first_name', models.CharField(default='John', max_length=30)),
                ('last_name', models.CharField(default='Appleseed', max_length=36)),
                ('date_of_birth', models.DateField(default='1900-01-01')),
                ('bio', models.TextField(blank=True)),
                ('email', models.EmailField(default='johnappleseed@example.com', max_length=254)),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
