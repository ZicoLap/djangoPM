from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from projects.models import Project, Task
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

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = forms.ProjectUpdateForm
    template_name = 'project/update.html'
    success_url = reverse_lazy('project_list')

    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.id])


class TaskCreateView(CreateView):
    model = Task
    fields = ['project', 'description']
    http_method_names = ['post']
    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.project.id])


class TaskUpdateView(UpdateView):
   model = Task
   fields = ['is_done']

   http_method_names = ['post']

   def get_success_url(self):
       return reverse_lazy('project_update', args=[self.object.project.id])


class TaskDeleteView(DeleteView):
    model = Task

    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.project.id])


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "project/delete.html"
    success_url = reverse_lazy('project_list')