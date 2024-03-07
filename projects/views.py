from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from models import Project, Task
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/list.html'
    paginate_by = 6

    def get_queryset(self):
        query_set = super().get_queryset()
        where = {'user_id': self.request.user}
        q = self.request.GET.get('q', None)
        if q is not None:
            where['title__icontains'] = q
        return query_set.filter(**where)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = forms.ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):
    model = Project
    form_class = forms.ProjectUpdateForm
    template_name = 'project/update.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.get_object().user_id == self.request.user.id

    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.id])


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Task
    fields = ['project', 'description']
    http_method_names = ['post']

    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return Project.objects.get(pk=project_id).user_id == self.request.user.id


    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.project.id])


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
   model = Task
   fields = ['is_done']

   http_method_names = ['post']

   def test_func(self):
       return self.get_object().project.user_id == self.request.user.id

   def get_success_url(self):
       return reverse_lazy('project_update', args=[self.object.project.id])


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Task

    def test_func(self):
        return self.get_object().project.user_id == self.request.user.id

    def get_success_url(self):
        return reverse_lazy('project_update', args=[self.object.project.id])


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Project
    template_name = "project/delete.html"


    def test_func(self):
        return self.get_object().user_id == self.request.user.id
    success_url = reverse_lazy('project_list')

