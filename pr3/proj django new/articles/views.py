from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse
from django.contrib import messages
from django_project import settings
import os 
from django.views.generic.detail import SingleObjectMixin

from .models import Article, Tag, Category
from .forms import ArticleForm

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self):
        queryset = Article.objects.select_related('category').prefetch_related('tags')
        search_query = self.request.GET.get('q', '')
        category_id = self.request.GET.get('category', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(context__icontains=search_query) |
                Q(excerpt__icontains=search_query) 
            )
        
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_q'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        return context
    
class ArticleByTagView(ArticleListView):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return super().get_queryset().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class ArticleByCategoryView(ArticleListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
    slug_field = 'slug'
    context_object_name = 'article'

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article 
    form_class = ArticleForm
    template_name = 'articles/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
    def get_success_url(self):
        return reverse('article.index')
    
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article 
    form_class = ArticleForm
    template_name = 'articles/update.html'
    pk_url_kwarg = 'article_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.get_object()
        return context
    
    def get_success_url(self):
        return reverse('article.update', args=(self.kwargs['article_id'],))
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "Вы не являетесь автором этой статьи.")
            return redirect('article.index')
        return super().dispatch(request, *args, **kwargs)
    
class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    pk_url_kwarg = 'article_id'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('article.index')
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "Вы не являетесь автором этой статьи.")
            return redirect('article.index')
        return super().dispatch(request, *args, **kwargs)    

class ArticleArchiveView(ListView):
    model = Article
    template_name = 'articles/archive.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.all_objects.filter(is_active=False)

class ArticleRestoreView(SingleObjectMixin, LoginRequiredMixin, View):
    model = Article
    queryset = Article.all_objects

    def post(self, request, pk):
        article = self.get_object()
        if article.author != request.user:
            messages.error(request, "Вы не автор этой статьи.")
            return redirect('article.archive')
        
        article.is_active = True
        article.save()
        messages.success(request, f'Статья "{article.name}" восстановлена!')
        return HttpResponseRedirect(reverse('article.archive'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "Вы не являетесь автором этой статьи.")
            return redirect('article.index')
        return super().dispatch(request, *args, **kwargs)

class ArticleForceDeleteView(SingleObjectMixin, LoginRequiredMixin, View):
    model = Article 
    queryset = Article.all_objects 

    def post(self, request, pk):
        article = self.get_object()
    def post(self, request, pk):
        try:
            article = Article.all_objects.get(pk=pk)
            if article.author != request.user:
                messages.error(request, "Вы не автор этой статьи.")
                return redirect('article.archive')
            
            article_name = article.name
            article.hard_delete()
            messages.success(request, f'Статья "{article_name}" полностью удалена!')
            return redirect('article.archive')
        except Article.DoesNotExist:
            messages.error(request, "Статья не найдена")
            return redirect('article.archive')
        except Exception as e:
            messages.error(request, f"Ошибка при удалении: {str(e)}")
            return redirect('article.archive')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "Вы не являетесь автором этой статьи.")
            return redirect('article.index')
        return super().dispatch(request, *args, **kwargs)

class FileDownloadView(View):
    def get(self, request):
        file_path = os.path.join(settings.MEDIA_ROOT, 'sample.pdf')
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="document.pdf"'
        return response

def page_not_found(request, exception):
    return render(request, 'articles/404.html', status=404)