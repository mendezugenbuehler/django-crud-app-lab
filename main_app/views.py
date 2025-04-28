from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Dog, Feeding
from .forms import FeedingForm

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Define the home view function
def home(request):
    return render(request, 'home.html')

# Define the about view function
def about(request):
    return render(request, 'about.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def dogs_index(request):
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html', { 'dogs': dogs })

@login_required
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    feeding_form = FeedingForm()
    return render(request, 'dogs/detail.html', {
        'dog': dog,
        'feeding_form': feeding_form
    })

@login_required
def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

@login_required
def dogs_create(request):
    if request.method == 'POST':
        dog = Dog(
            name=request.POST['name'],
            breed=request.POST['breed'],
            description=request.POST['description'],
            age=request.POST['age'],
            user=request.user
        )
        dog.save()
        return redirect('detail', dog.id)
    return render(request, 'dogs/dog_form.html')

@login_required
def dogs_update(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    if request.method == 'POST':
        dog.name = request.POST['name']
        dog.breed = request.POST['breed']
        dog.description = request.POST['description']
        dog.age = request.POST['age']
        dog.save()
        return redirect('detail', dog.id)
    return render(request, 'dogs/dog_form.html', { 'object': dog })

@login_required
def dogs_delete(request, dog_id):
    Dog.objects.get(id=dog_id).delete()
    return redirect('index')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)