from django import forms

import datetime

from . import models

class TodoForm(forms.ModelForm):

    class Meta:
        model = models.Todo
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'due_time': forms.DateInput(
                attrs={'type': 'date', 'min': datetime.datetime.now().date()})
        }

    def clean_due_time(self):
        due_time = self.cleaned_data['due_time']
        if due_time < datetime.date.today():
            raise forms.ValidationError("The due_time cannot be in the past!")
        return due_time
