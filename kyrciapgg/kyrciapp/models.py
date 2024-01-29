from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    # additional_field = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'custom_user'
