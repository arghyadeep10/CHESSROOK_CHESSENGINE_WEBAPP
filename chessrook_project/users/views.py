from django.shortcuts import render
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('/home_page')
    else:
        if request.method == 'POST':
            # we are getting a form submission
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                # since form is valid we send a one time success message
                username = form.cleaned_data.get('username')
                messages.success(request, f"Account Created for username: {username}. You can now login.")
                return HttpResponseRedirect(reverse("login"))
            
        else:
            # it is a GET request, create a new form and render it
            form = UserRegistrationForm()
        return render(request, 'users/register.html', {
            'form':form
        })

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        # we are getting a form submission
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # since form is valid we send a one time success message
            messages.success(request, f"Account Details Updated Successfully.")
            return HttpResponseRedirect(reverse("profile"))
        
    else:
        # it is a GET request, create a new form and render it
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {
        'form':form
    })