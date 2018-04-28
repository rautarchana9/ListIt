from django.db import models
from django.utils import timezone
from django.conf import settings

import datetime

# Create your models here.

class List(models.Model):
  title = models.CharField(max_length=60)
  slug = models.SlugField(max_length=60,editable=False)

  def __str__(self):
    return '%s' % (self.name)

  class Meta:
    ordering = ['title']

class Task(models.Model):
  title = models.CharField(max_length=60)
  body = models.TextField()
  created_at = models.DateField(default=timezone.now, blank=True, null=True)
  due_date = models.DateField(blank=True, null=True)
  completed = models.BooleanField(default=False)
  completed_at = models.DateField(blank=True, null=True)
  todo_list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)

  def __str__(self):
        return '%s %s' % (self.title, self.body)
  
  class Meta:
    get_latest_by = ['due_date']


class Subtask(models.Model):
  title = models.CharField(max_length=200)
  todo_note = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return '%s' % (self.title)

