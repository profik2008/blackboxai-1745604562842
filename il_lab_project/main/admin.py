
# main/admin.py
from django.contrib import admin
from .models import Contact, Newsletter, BlogPost, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date', 'is_actual')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_actual', 'date')
    search_fields = ('title',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)
    readonly_fields = ('subscribed_at',)