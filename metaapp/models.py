from django.db import models

class SidebarWidget(models.Model):
    placement = models.IntegerField()
    title = models.CharField(max_length=128)
    show_title = models.BooleanField(default=False)
    contents = models.TextField()
    
    def __unicode__(self):
        return self.title


