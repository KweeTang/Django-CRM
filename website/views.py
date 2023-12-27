from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):

    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          messages.success(request, "You Have Been Logged On")
          return redirect('home')
        else:
          messages.success(request, "There was an Error")
          return redirect('home')

    return render(request, 'home.html', {'records': records})

#def login_user(request):
#    pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
       form = SignUpForm(request.POST)
       if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        # Look up records
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success (request, "Record Deleted Successfully")
        return redirect ('home')
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')
    
def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "You Have Successfully Added Record")
                return redirect('home')
        else:
            form = AddRecordForm()
            return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        # Look up current record
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success (request, "Record Updated Successfully")
            return redirect ('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')
    

    
