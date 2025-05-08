from django.contrib import admin
from .models import Article, Tag, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'is_active', 'category')  
    list_editable = ('is_active',)  
    list_filter = ('created_at', 'category', 'is_active')  
    search_fields = ('name', 'content')  
    prepopulated_fields = {"slug": ["name"]}  
    readonly_fields = ('created_at', 'updated_at')  

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
