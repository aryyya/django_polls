from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        time_now = timezone.now()
        return time_now - datetime.timedelta(days=1) <= self.pub_date <= time_now
    
    def was_published_in_the_future(self):
        time_now = timezone.now()
        return time_now < self.pub_date

    def was_published_in_the_past(self):
        return not self.was_published_in_the_future()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
