from haystack import indexes
from .models import Asset


class AssetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    file = indexes.CharField(model_attr='file')

    def get_model(self):
        return Asset

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
