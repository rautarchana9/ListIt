from django.contrib import admin
from datetime import date, timedelta

# Register your models here.
from .models import List, Task, Subtask
from django.utils.translation import gettext_lazy as _

class ItemInline(admin.StackedInline):
  model = Subtask
  extra = 3
class CustomDueDateFilter(admin.SimpleListFilter):
  title = ('Due date')

  parameter_name = 'due_date'

  def lookups(self, request, model_admin):
    return (('A',  _('Today')),
            ('B',_('This week')),
            ('C',_('Next week')),
            ('D', _('Overdue')),
            )
         
  def queryset(self, request, queryset):
    t = date.today()
    if self.value() == 'A':
      return queryset.filter(due_date=t)
    if self.value() == 'B':
      return queryset.filter(due_date__gte=t, due_date__lte=t+timedelta(days=8))
    if self.value() == 'C':
      return queryset.filter(due_date__gte=t+timedelta(days=8), due_date__lte=t+timedelta(days=15))
    if self.value() == 'D':
      return queryset.filter(due_date__lt=t+timedelta(days=-1))

class TaskAdmin(admin.ModelAdmin):
  fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['due_date']}),
        ('status', {'fields': ['status']})
    ]

  list_display = ('title', 'due_date', 'status')
  list_filter = [CustomDueDateFilter]
  search_fields = ['title']
  inlines = [ItemInline]
admin.site.register(Task, TaskAdmin)
admin.site.register(List)

