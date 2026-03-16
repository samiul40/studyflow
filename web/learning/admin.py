from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin

from .models import LearningResource, LearningUnit


class LearningUnitInline(SortableInlineAdminMixin, admin.TabularInline):
    model = LearningUnit
    extra = 0
    fields = (
        "order",
        "title",
        "duration_minutes",
        "status",
        "video_progress_minutes",
    )
    ordering = ("order",)


@admin.register(LearningResource)
class LearningResourceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title", "resource_type", "user", "progress", "created_at")
    list_filter = (
        "resource_type",
        "created_at",
    )
    search_fields = ("title", "description", "user__username")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [LearningUnitInline]

    date_hierarchy = "created_at"

    autocomplete_fields = ("user",)

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "title", "resource_type", "description"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Progress")
    def progress(self, obj):
        total = obj.units.count()
        if total == 0:
            return "0%"
        completed = obj.units.filter(status="completed").count()
        percentage = int((completed / total) * 100)
        return f"{completed}/{total} ({percentage}%)"


@admin.register(LearningUnit)
class LearningUnitAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "resource",
        "order",
        "status",
        "duration_minutes",
        "video_progress_minutes",
    )
    list_filter = (
        "status",
        "resource__resource_type",
    )
    search_fields = ("title", "resource__title", "notes")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("resource", "order")

    autocomplete_fields = ("resource",)

    fieldsets = (
        (
            None,
            {
                "fields": ("resource", "title", "order", "status"),
            },
        ),
        (
            "Progress",
            {
                "fields": ("duration_minutes", "video_progress_minutes", "notes"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
