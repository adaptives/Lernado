from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    location = models.CharField(max_length=64, blank=True)
    profile_picture = models.ImageField(upload_to='images/userpics', blank=True)
    
    def __unicode__(self):
        return ("%s %s %r") % (self.user.username, self.location, self.profile_picture)
    

def create_user_profile(sender, instance, created, **kwargs):
    try:
        """
        When a user profile is created, the User object is updated, which
        causes the signal to be send once again and as a result this function
        will also be called.
        """
        UserProfile.objects.get(user=instance)
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)



