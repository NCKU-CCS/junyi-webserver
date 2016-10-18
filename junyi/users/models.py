from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    email = models.EmailField(primary_key=True)
    fb_id = models.TextField()
    name = models.TextField()
    link = models.URLField()
    gender = models.TextField()
    locale = models.TextField()
    picture_url = models.URLField()
    timezone = models.TextField()
    access_token = models.TextField()

    def __str__(self):
        return "%s %s" % (str(self.pk), self.name)
