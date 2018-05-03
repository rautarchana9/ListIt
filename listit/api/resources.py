from tastypie.resources import ModelResource
from listit.models import Task, Subtask


class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        allowed_methods = ['get']
