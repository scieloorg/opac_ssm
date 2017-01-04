from django.shortcuts import render

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
            new_file.save()
            form = FileFieldForm()
            return render(request, 'pages/home.html', {'form': form})
    else:
        form = FileFieldForm()
    return render(request, 'pages/upload.html', {'form': form})
