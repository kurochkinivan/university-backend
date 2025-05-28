from django.db import models
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags 
from django.urls import reverse
from django.contrib.auth import get_user_model

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True 

    def delete(self):
        self.is_active = False 
        self.save()

class TimeStampModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
  updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

  class Meta:
    abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        abstract = True 

    def save(self, *args, **kwargs):
        if not self.slug:
            attr = getattr(self, 'name', '')
            self.slug = slugify(attr)

        return super().save(*args, **kwargs)

class Category(SlugModel):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Tag(SlugModel):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название тега")

    def __str__(self):
        return self.name

class Article(TimeStampModel, SlugModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название статьи")
    content = CKEditor5Field(verbose_name='Описание', config_name='extends')
    excerpt = models.TextField(verbose_name='Отрывок', blank=True)
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/", verbose_name="Изображение")
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")


    class Meta:
        ordering = ['-created_at']
    
    def hard_delete(self):
        image_name = self.featured_image.name if self.featured_image else None
        super(SoftDeleteModel, self).delete()
        if image_name and image_name != "default.jpg":
            try:
                storage = self.featured_image.storage
                if storage.exists(image_name):
                    storage.delete(image_name)
            except Exception as e:
               print(f"Ошибка при удалении файла {image_name}: {e}")

    def get_absolute_url(self):
        return reverse('article.detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.excerpt and self.content:
            plaint_text = strip_tags(self.content)
            self.excerpt = plaint_text[:min(100, len(plaint_text))] + '...'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name