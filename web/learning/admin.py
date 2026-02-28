from django.contrib import admin

from .models import LearningResource, LearningUnit


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "created_at", "updated_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(LearningUnit)
class LearningUnitAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "status", "created_at", "updated_at")
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
