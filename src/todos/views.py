from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms.models import model_to_dict

from . import forms, models
# Create your views here.

def index(request):
    url_params = request.GET.dict()
    # We don't need page, if we will use the page key, when we will use sort and after this
    # we will go to another page we will have error
    _ = url_params.pop('page', None)

    # Order_by only if we have priority key or due_time key
    todos = []
    if not request.user.is_anonymous:
        todo_list = (models.Todo.objects.filter(user=request.user) if not url_params.values()
                        else models.Todo.objects.filter(user=request.user).order_by(*url_params.values()))

        paginator = Paginator(todo_list, 10)
        page = request.GET.get('page')
        todos = paginator.get_page(page)

    form_data = {k:escape(v) for (k,v) in request.POST.items()}
    form = forms.TodoForm(form_data or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('todos:index'))

    # Show new form only if we don't have errors from POST, prev form
    # because we need to show errors from prev form if we have some errors
    if not form.errors:
        form = forms.TodoForm(initial={'user': request.user})

    context = {
        'form': form,
        'todos': todos,
        'priority': request.GET.get('priority', None),
        'due_time': request.GET.get('due_time', None)
    }

    return render(request, 'todos/index.html', context)


def clean(request):
    return HttpResponseRedirect(reverse('todos:index'))


@login_required
def edit(request, todo_id=None):
    todo = models.Todo.objects.get(pk=request.POST.get('id', todo_id))
    form_data = {k:escape(v) for (k,v) in request.POST.items()}

    form = forms.TodoForm(form_data or None, instance=todo)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('todos:index'))

    form = forms.TodoForm(initial=model_to_dict(todo), instance=todo)
    context = {
        'form': form,
        'todo_id': todo.id
    }
    return render(request, 'todos/edit.html', context)


@login_required
def delete(request, todo_id):
    models.Todo.objects.get(pk=todo_id).delete()
    return HttpResponseRedirect(reverse('todos:index'))
