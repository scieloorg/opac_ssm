from django.shortcuts import render
from datetime import date
from haystack.generic_views import SearchView
from .forms import FileFieldForm
from .models import Asset


def home(request):
    context = {}
    return render(request, 'pages/home.html', context)


def upload(request):

    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = Asset(file=request.FILES['file'])
            new_file.owned_by = request.user
            # cd = form.cleaned_data
            # new_file.name = cd['name']
            # new_file.description = cd['description']
            # new_file.school = cd['school']
            # new_file.subject = cd['subject']
            # new_file.price = cd['price']
            # new_file.rating = '0.0'
            # new_file.user = request.user
            new_file.save()
            form = FileFieldForm()
            return render(request, 'pages/home.html', {'form': form})
    else:
        form = FileFieldForm()
    return render(request, 'pages/upload.html', {'form': form})


class MySearchView(SearchView):
    """My custom search view."""

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        return context
