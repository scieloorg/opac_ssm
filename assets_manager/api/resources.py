# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from haystack.inputs import Raw
from haystack.query import SearchQuerySet
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.authentication import (
    BasicAuthentication,
    ApiKeyAuthentication,
    SessionAuthentication,
    MultiAuthentication)
from tastypie.authorization import ReadOnlyAuthorization

from django.conf import settings

from assets_manager.models import Asset


class AssetResource(ModelResource):

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/search%s$" % (
                    self._meta.resource_name, trailing_slash),
                self.wrap_view('get_search'),
                name="api_get_search"
            ),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Asset).load_all().filter(
             content=Raw(request.GET.get('q', ''))
        )
        limit_per_page = getattr(settings, 'API_LIMIT_PER_PAGE', 20)
        paginator = Paginator(sqs, limit_per_page)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        limit = page.paginator.per_page
        offset = limit * (page.number - 1)
        total_count = page.paginator.count

        meta = {
            'offset': offset,
            'limit': limit,
            'total_count': total_count,
        }

        if page.has_next():
            meta['next'] = page.next_page_number()
        else:
            meta['next'] = None

        if page.has_previous():
            meta['previous'] = page.previous_page_number()
        else:
            meta['previous'] = None

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'meta': meta,
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    class Meta:
        resource_name = 'asset'
        queryset = Asset.objects.all()
        allowed_methods = ['get']

        authentication = MultiAuthentication(
            BasicAuthentication(),
            SessionAuthentication(),
            ApiKeyAuthentication()
        )

        authorization = ReadOnlyAuthorization()
