from django.urls import path
from .views import HomeView, ManageCourseListView, CourseCreateView, \
    CourseUpdateView, CourseDetailView, CourseDeleteView, StudentCourseListView, StudentCourseDetailView, \
    DocumentDeleteView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('courses/main', ManageCourseListView.as_view(), name='course_list_view'),
    path('course/create', CourseCreateView.as_view(), name='course_create'),
    path('course/edit/<slug:slug>', CourseUpdateView.as_view(), name='course_edit'),
    path('course/delete/<slug:slug>', CourseDeleteView.as_view(), name='course_delete'),
    path('course/<slug:slug>', CourseDetailView.as_view(), name='course_detail'),
    path('file/<slug:slug>', views.model_form_upload, name='upload'),
    path('document/<slug:slug>', views.document_list, name='document'),
    path('document/delete/<int:pk>', DocumentDeleteView.as_view(), name='document_delete'),
    path('student/courses', StudentCourseListView.as_view(), name='student_course_list_view'),
    path('student/course/<slug:slug>', StudentCourseDetailView.as_view(), name="student_course_detail")

]