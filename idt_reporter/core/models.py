from django.db import models

class Done(models.Model):
    done_id =  models.IntegerField(default=None)
    owner = models.CharField(max_length=64)
    team_short_name = models.CharField(max_length=64)
    done_date = models.DateField(default=None)
    last_updated = models.DateTimeField(default=None)
    is_goal = models.BooleanField(default=None)
    is_completed = models.BooleanField(default=None)
    raw_text = models.TextField(default=None)
    markedup_text = models.TextField(default=None)

    def __unicode__(self):
        return str(self.done_id)
