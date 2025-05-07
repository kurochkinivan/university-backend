from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles, name="article.index"), 
    path('create/', views.article_create, name="article.create"),
    path('update/<int:article_id>/', views.article_update, name="article.update"),
    path('remove/<int:article_id>/', views.article_delete, name="article.delete"),
    path('file-download/', views.file_download, name="article.file_download"),

    path('tag/<slug:tag_slug>/', views.articles_by_tag, name="article.tag"),
    path('category/<slug:category_slug>/', views.articles_by_category, name="article.category"),
    
    path('<slug:slug>/', views.article_detail, name='article.detail'),
]