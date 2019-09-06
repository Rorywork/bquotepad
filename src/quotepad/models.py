from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class Document(models.Model):
    user = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    document = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
	    return "user_%s - %s" % (self.user, self.description)    


class Profile(models.Model):
    user            =   models.OneToOneField(User, on_delete=models.CASCADE)
    first_name      =   models.CharField(max_length=40)
    last_name       =   models.CharField(max_length=60)
    company_name    =   models.CharField(max_length=60)
    email           =   models.CharField(max_length=60)
    telephone       =   models.CharField(max_length=20)
    cur_quote_no    =   models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username
     
