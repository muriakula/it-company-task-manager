from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Task, TaskType, Position, Worker

# Додаємо TaskType до адміністрування
admin.site.register(TaskType)

# Додаємо Position до адміністрування
admin.site.register(Position)


# Спеціальна конфігурація для адміністрування користувачів Worker
@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": ("first_name", "last_name", "position"),
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "priority", "deadline", "is_completed", "task_type")
    list_filter = ("priority", "is_completed", "task_type")
    search_fields = ("name", "description", "task_type__name", "assignees__first_name", "assignees__last_name")
    date_hierarchy = "deadline"
