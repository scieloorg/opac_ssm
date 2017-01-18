from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import FileFieldForm
from .models import Asset


@login_required
def home(request):
    context = {}
    return render(request, 'pages/home.html', context)


@login_required
def upload(request):

    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = Asset(file=request.FILES['file'])
            new_file.metadata = {'foo': 'bar'}
            new_file.save()
            form = FileFieldForm()
            return render(request, 'pages/home.html', {'form': form})
    else:
        form = FileFieldForm()
    return render(request, 'pages/upload.html', {'form': form})
