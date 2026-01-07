from django.contrib import admin
from .models import NewsPost

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):  # <--- Change to this
    list_display = ('title', 'category', 'date_posted', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'summary')