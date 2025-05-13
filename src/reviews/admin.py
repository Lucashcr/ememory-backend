from django.contrib import admin

from reviews.models import ReviewInfo, ReviewSchedule, Subject

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "user")
    search_fields = ("name",)
    list_filter = ("user",)
    ordering = ("name",)
    list_per_page = 20
    list_display_links = ("name",)
    autocomplete_fields = ("user",)


@admin.register(ReviewInfo)
class ReviewInfoAdmin(admin.ModelAdmin):
    list_display = ("topic", "user", "subject__name", "initial_date")
    search_fields = ("topic",)
    list_filter = ("user",)
    ordering = ("topic",)
    list_per_page = 20
    list_display_links = ("topic",)
    list_select_related = ("user",)
    autocomplete_fields = ("subject","user",)

    
@admin.register(ReviewSchedule)
class ReviewScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "review_info__topic", "review_info__user__email", "scheduled_for", "status")
    search_fields = ("review_info__topic",)
    list_filter = ("status",)
    ordering = ("-scheduled_for",)
    list_per_page = 20
    list_display_links = ("review_info__topic",)
    list_editable = ("status",)
