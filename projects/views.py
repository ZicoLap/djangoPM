from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from projects.models import Project, Task
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/list.html'
    paginate_by = 6

    def get_queryset(self):
        query_set = super().get_queryset()
        where = {}
        q = self.request.GET.get('q', None)
        if q is not None:
            where['title__icontains'] = q
        return query_set.filter(**where)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = forms.ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list')

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = forms.ProjectUpdateForm
    template_name = 'project/update.html'
    success_url = reverse_lazy('project_list')

    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.id])


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['project', 'description']
    http_method_names = ['post']
    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.project.id])


class TaskUpdateView(LoginRequiredMixin,  UpdateView):
   model = Task
   fields = ['is_done']

   http_method_names = ['post']

   def get_success_url(self):
       return reverse_lazy('project_update', args=[self.object.project.id])


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.project.id])


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "project/delete.html"
    success_url = reverse_lazy('project_list')