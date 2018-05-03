from tastypie.resources import ModelResource
from listit.models import Task, Subtask
from tastypie.authorization import Authorization


class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        authorization = Authorization()
