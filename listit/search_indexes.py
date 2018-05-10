import datetime
from haystack import indexes
from listit.models import Task


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    due_date = indexes.DateTimeField(model_attr='due_date')
    def get_model(self):
        return Task

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.order_by('due_date')
