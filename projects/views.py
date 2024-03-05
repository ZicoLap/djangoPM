from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from projects.models import Project
from . import forms


# Create your views here.
class ProjectListView(ListView):
    model = Project
    template_name = 'project/list.html'


class ProjectCreateView(CreateView):
    model = Project
    form_class = forms.ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list')