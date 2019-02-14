from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import escape

def signup(request):
    form_data = {k:escape(v) for (k,v) in request.POST.items()}
    form = UserCreationForm(form_data or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('todos:index'))

    return render(request, 'signup.html', {'form': form})
