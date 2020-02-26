from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from slugify import slugify

from tasks.translater import translate

def make_unique_slug(model, text, counter=0):
    try:
        text = translate(text)
    except:
        print('Сервис перевода не доступен')
    slug = slugify(text)
    str_counter = ''
    if slug == 'create':
        slug = 'create0'
    if counter:
        str_counter = str(counter)
    if model.objects.filter(slug=slug+str_counter).count():
        counter += 1
        slug = make_unique_slug(model, slug, counter)
    return slug + str_counter


class Category(models.Model):
    slug = models.CharField(default='_', max_length=128)
    name = models.CharField(max_length=256)
    todos_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.slug})'
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = make_unique_slug(Category, self.name)
        super(Category, self).save(*args, **kwargs)

class Priority(models.Model):
    slug = models.CharField(default='_', max_length=128)
    name = models.CharField(max_length=256)
    todos_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'

    def __str__(self):
        return f'{self.name} ({self.slug})'
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = make_unique_slug(Priority, self.name)
        super(Priority, self).save(*args, **kwargs)

class TodoItem(models.Model):
    # PRIORITY_HIGH = 1
    # PRIORITY_MEDIUM = 2
    # PRIORITY_LOW = 3

    # PRIORITY_CHOICES = [
    #     (PRIORITY_HIGH, "Высокий приоритет"),
    #     (PRIORITY_MEDIUM, "Средний приоритет"),
    #     (PRIORITY_LOW, "Низкий приоритет"),
    # ]

    description = models.TextField("описание")
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    # old_priority = models.IntegerField(
    #     "Приоритет", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    # )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=True,
        null=True,
    )
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])
