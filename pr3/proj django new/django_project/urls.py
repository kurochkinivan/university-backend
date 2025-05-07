from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from articles.views import page_not_found  

handler404 = page_not_found

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('posts/', include('blogs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path('test404/', page_not_found, {'exception': Exception('Test')})]