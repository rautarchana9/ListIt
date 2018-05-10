from tastypie.resources import ModelResource
from django.db.models import Q
from datetime import date, datetime, timedelta


class ModelResourceCustom(ModelResource):

    def build_filters(self, filters=None):
        """Allow for building of custom filters based on url keyword."""
        custom_filters = self._meta.custom_filters
        custom_queries = {}

        for filter_id, filter_method in custom_filters.items():
            built_filter = filter_method(filters)
            if built_filter:
                custom_queries[filter_id] = built_filter

        orm_filters = super(ModelResourceCustom, self).build_filters(filters)
        for query_id, query in custom_queries.items():
            orm_filters[query_id] = query
        return orm_filters

    def apply_filters(self, request, applicable_filters):
        """Allow for the application of custom filters built in the build_filters method"""
        custom_built_queries = [filter_id for filter_id in self._meta.custom_filters.keys()]
        post_filters = []
        for key in list(applicable_filters):
            if key in custom_built_queries:
                post_filters.append(applicable_filters.pop(key))

        filtered = super(ModelResourceCustom, self).apply_filters(request, applicable_filters)
        for post_filter in post_filters:
            filtered = filtered.filter(post_filter)

        return filtered


def get_start_end(next=False):
    today = date.today()
    if next:
        start = today + timedelta(days = 7 - today.weekday())
        end = start + timedelta(days = 6)
    else:
        start = today
        week_start = today - timedelta(days = today.weekday())
        end = week_start + timedelta(days = 6)

    return (start, end)


def custom_duedate(url_args):
    try:
        duedate = url_args.pop('duedate')[0]
    except KeyError:
        return None

    if duedate == "today":
        query = (
                    Q(due_date__exact=date.today())
                )
    elif duedate == "overdue":
        query = (
                    Q(due_date__lt=date.today())
                )
    else:
        if duedate == "this_week":
            (start, end) = get_start_end()
        if duedate == "next_week":
            (start, end) = get_start_end(True)
        query = (
                    Q(due_date__gte=start) & Q(due_date__lte=end)
                )
    return query

#Group a few filters for use in a custom filters set.
custom_filter_group = {'due_date' : custom_duedate}      
