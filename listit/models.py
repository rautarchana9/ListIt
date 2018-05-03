from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings
import datetime
from model_utils.fields import StatusField
from model_utils import Choices
from djchoices import DjangoChoices, ChoiceItem

# Create your models here.

class List(models.Model):
  title = models.CharField(max_length=60)
  slug = models.SlugField(max_length=60,editable=False)

  def __str__(self):
    return '%s' % (self.title)

  class Meta:
    ordering = ['title']


class SoftDeletionQuerySet(QuerySet):
  def delete(self):
      return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

  def hard_delete(self):
      return super(SoftDeletionQuerySet, self).delete()

  def alive(self):
      return self.filter(deleted_at=None)

  def dead(self):
      return self.exclude(deleted_at=None)

class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
          return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()

class Task(SoftDeletionModel):

  objects = SoftDeletionManager()

  STATUS_TYPE = (
        ("C", "Completed"),
        ("P", "Pending"),
        )
  title = models.CharField(max_length=60)
  due_date = models.DateField(null=True, blank=True)
  todo_list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
  status = models.CharField(max_length=1, choices=STATUS_TYPE, null=True)
  def __str__(self):
        return ' %s' % (self.title)
  
  class Meta:
    ordering = ['due_date']

class Subtask(models.Model):
  title = models.CharField(max_length=200)
  todo_note = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return '%s' % (self.title)

