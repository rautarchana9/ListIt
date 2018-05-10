from tastypie.resources import ModelResource
from listit.models import Task, Subtask
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from haystack.query import SearchQuerySet
from django.conf.urls import url, include
from tastypie.exceptions import BadRequest

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'tasks'
        fields = ['title', 'due_date', 'status']
        filtering = {
            'due_date': ['exact', 'lt', 'lte', 'gte', 'gt']
            }
        ordering = ['due_date']
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Task).load_all().auto_query(request.GET.get('q', ''))
        #paginator = Paginator(request.GET, sqs, limit=20)

        #try:
        #    page = paginator.page()
        #except InvalidPage:
        #    raise Http404("Sorry, no results on that page.")

        #objects = []

        #for result in page.object_list:
        #    bundle = self.build_bundle(obj=result.object, request=request)
        #    bundle = self.full_dehydrate(bundle)
        #    objects.append(bundle)

        #object_list = {
        #    'objects': objects,
        #}

        #self.log_throttled_access(request)
        #return self.create_response(request, object_list) 
        paginator = self._meta.paginator_class(request.GET, sqs,
            resource_uri=self.get_resource_uri(), limit=self._meta.limit,
            max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)

        to_be_serialized = paginator.page()
        bundles = [self.build_bundle(obj=result.object, request=request) for result in to_be_serialized['objects']]
        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)
