from django.db import models
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags 

class Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="Слаг категории")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название тега")
    slug = models.SlugField(unique=True, verbose_name="Слаг тега")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название статьи")
    content = CKEditor5Field(verbose_name='Описание', config_name='extends')
    excerpt = models.TextField(verbose_name='Отрывок', blank=True)
    featured_image = models.ImageField(
        blank=True, default="default.jpg", upload_to="images/", verbose_name="Изображение"
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг статьи")
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if not self.excerpt:
            plaint_text = strip_tags(self.content)
            self.excerpt = plaint_text[:min(100, len(plaint_text))] + '...'

        print(self.slug)

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
