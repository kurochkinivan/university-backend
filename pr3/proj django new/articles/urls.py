from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    FileDownloadView,
    ArticleArchiveView,
    ArticleRestoreView,
    ArticleForceDeleteView,
    ArticleByTagView,
    ArticleByCategoryView,
    page_not_found
)

urlpatterns = [
    path('', ArticleListView.as_view(), name="article.index"),
    
    path('create/', ArticleCreateView.as_view(), name="article.create"),
    path('update/<int:article_id>/', ArticleUpdateView.as_view(), name="article.update"), 
    path('remove/<int:article_id>/', ArticleDeleteView.as_view(), name="article.delete"),
    path('file-download/', FileDownloadView.as_view(), name="article.file_download"),

    path('archive/', ArticleArchiveView.as_view(), name='article.archive'),
    path('<int:pk>/restore/', ArticleRestoreView.as_view(), name='article.restore'),
    path('<int:pk>/force-delete/', ArticleForceDeleteView.as_view(), name='article.force_delete'),

    path('tag/<slug:tag_slug>/', ArticleByTagView.as_view(), name="article.tag"),
    path('category/<slug:category_slug>/', ArticleByCategoryView.as_view(), name="article.category"),
    
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article.detail'),
]

handler404 = page_not_found