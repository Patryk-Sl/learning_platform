from django.contrib.auth.models import User
from django.views.generic import DetailView

from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document


def document_list(request, slug):
    documents = Document.objects.all().filter(course__slug=slug)
    return render(request, 'file/document.html', {'documents': documents})


def model_form_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.course = course
            new_form.save()
            form.save()
            return redirect('course_list_view')
    else:
        form = DocumentForm()
    return render(request, 'file/upload.html', {'form': form})


class DocumentDeleteView(DeleteView):
    model = Document
    template_name = 'file/document_delete.html'
    success_url = reverse_lazy('course_list_view')


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        form.instance.students.set(self.request.POST.getlist('students'))
        form.save()
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['title', 'overview']
    success_url = reverse_lazy('course_list_view')


class HomeView(ListView):
    model = Course
    template_name = "home.html"
    context_object_name = 'courses'

    def get_queryset(self):
        qs = super(HomeView, self).get_queryset()
        return qs.all()


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['title', 'overview']
    success_url = reverse_lazy('course_list_view')
    template_name = 'courses/teachers/courses_create.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/teachers/course_list_view.html'
    context_object_name = 'courses'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = User.objects.filter(groups__name__in=['students'])
        context['students'] = students
        return context


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = User.objects.filter(groups__name__in=['students'])
        context['students'] = students
        return context


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'courses/teachers/course_delete.html'
    success_url = reverse_lazy('course_list_view')
    permission_required = 'courses.delete_course'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/teachers/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        documents = Document.objects.all().filter(course__slug=course.slug)
        context['documents'] = documents
        return context


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/students/list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        x = qs.filter(students__in=[self.request.user])
        return x


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/students/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        x = qs.filter(students__in=[self.request.user])
        return x

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        documents = Document.objects.all().filter(course__slug=course.slug)
        context['documents'] = documents
        return context
