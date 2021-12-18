from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from .models import Profile
from .forms import UserRegistrationForm, UserForm, ProfileForm


def home(request):
    return render(request, 'account/home.html')


def success_change(request):
    return render(request, 'account/success.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Saved everything well')
        else:
            messages.error(request, 'Something went wrong')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


class UserListView(ListView):
    model = Profile
    template_name = 'account/profile_list.html'
