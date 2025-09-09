
from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    
    # --- IMPORTANT: DEFINE YOUR SUPERUSER DETAILS HERE ---
    USERNAME = 'admin'
    EMAIL = 'admin@example.com'
    PASSWORD = 'your-super-secret-password'
    # ----------------------------------------------------

    if not User.objects.filter(username=USERNAME).exists():
        print(f'Creating new superuser: {USERNAME}')
        User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )
    else:
        print(f'Superuser {USERNAME} already exists. Skipping.')

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'), # Make sure this matches your previous migration
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]