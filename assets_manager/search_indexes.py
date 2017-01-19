# -*- coding: utf-8 -*-
import json
import logging

from haystack import indexes

from .models import Asset, AssetBucket

logger = logging.getLogger(__name__)


class AssetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Asset

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare(self, object):
        self.prepared_data = super(AssetIndex, self).prepare(object)

        if object.metadata:
            try:
                metadata = json.loads(object.metadata.replace("'", "\""))
            except TypeError as e:
                logger.error(e)
                raise

            for key, val in metadata.items():
                if isinstance(val, str):
                    self.prepared_data[key] = val

        return self.prepared_data


class AssetBucketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return AssetBucket

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
