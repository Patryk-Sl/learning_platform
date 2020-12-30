
from django.contrib import admin
from .models import Course, Module


class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    list_filter = ['created']
    search_fields = ['title', 'overview','students']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]



# stary sposob rejestracji do admina
# admin.site.register(Subject)
# admin.site.register(Course)
# admin.site.register(Module)