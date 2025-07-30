from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='kusso_profile')
    authenticated_at = models.DateTimeField()
    data = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
