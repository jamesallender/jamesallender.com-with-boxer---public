from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    # Post requests
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request=request, message=f'Account created for {username}!')
            form.save()
            return redirect(to='home')
        else:
            messages.error(request=request, message=f'invalid account info')


    # GET requests
    else:
        form = UserRegisterForm()
    return render(request=request, template_name='users/register.html', context={'form': form})


def about(request):
    return render(request=request, template_name='users/about.html')
