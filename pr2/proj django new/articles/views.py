from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from django_project import settings
from .models import Article, Tag, Category
from django.http import HttpResponseRedirect, FileResponse
from .forms import ArticleForm
import os


def get_articles_queryset(request):
    """Общая функция для получения отфильтрованных статей"""
    articles = Article.objects.all()
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    if search_query:
        articles = articles.filter(
            Q(name__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query))
    
    if category_id:
        articles = articles.filter(category__id=category_id)
    
    return articles


def articles(request):
    articles = get_articles_queryset(request)
    categories = Category.objects.all() 

    return render(request, 'articles/index.html', {
        "articles": articles,
        "categories": categories,
        "search_query": request.GET.get('q', ''),
        "selected_category": request.GET.get('category', ''),
    })


def articles_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    articles = Article.objects.filter(tags=tag)
    categories = Category.objects.all()  # Добавляем категории
    
    return render(request, 'articles/index.html', {
        "articles": articles,
        "categories": categories
    })


def articles_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    articles = Article.objects.filter(category=category)
    categories = Category.objects.all()  # Добавляем категории
    
    return render(request, 'articles/index.html', {
        "articles": articles,
        "categories": categories
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'articles/detail.html', {'article': article})


def article_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            messages.success(request, "Статья успешно создана!")
            return HttpResponseRedirect(reverse('article.index'))
    else:
        article_form = ArticleForm()
    return render(request, 'articles/create.html', {'article_form': article_form})


def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse('article.update', args=(article_id,)))
    else:
        article_form = ArticleForm(instance=article)
    return render(request, 'articles/update.html', {
        "article_form": article_form,
        "article": article
    })


def article_delete(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        article.delete()
        return HttpResponseRedirect(reverse('article.index'))
    return HttpResponseRedirect(reverse('article.index'))


def file_download(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'sample.pdf')
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="document.pdf"'
    return response

def page_not_found(request, exception):
    return render(request, 'articles/404.html', status=404)