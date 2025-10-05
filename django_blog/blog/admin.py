from django.contrib import admin
from .models import Post, Profile

admin.site.register(Post)
admin.site.register(Profile)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('published_date',)

# Only register Profile manually
admin.site.register(Profile)