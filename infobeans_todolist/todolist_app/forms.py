from django import forms
from .models import TodoList

class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['task_title', 'task_description', 'task_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['task_description'].widget.attrs.update({'class':'form-control'})
