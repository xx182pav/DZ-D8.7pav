from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from django.views.decorators.cache import cache_page

from django.core.cache import cache

from tasks.models import TodoItem, Category, Priority
from collections import Counter
from datetime import datetime


def index(request):

    # 1st version
    # counts = {t.name: random.randint(1, 100) for t in Tag.objects.all()}

    # 2nd version
    # counts = {t.name: t.taggit_taggeditem_items.count()
    # for t in Tag.objects.all()}

    # 3rd version
    # from django.db.models import Count

    # counts = Category.objects.annotate(total_tasks=Count(
    #     'todoitem')).order_by("-total_tasks")
    # counts = {c.name: c.total_tasks for c in counts}

    # return render(request, "tasks/index.html", {"counts": counts})

    # 4 version

    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.user:
        user = request.user
    else:
        user = None

    # priority_counters = Counter()
    # tasks = TodoItem.objects.all()
    # for task in tasks:
    #     priority_counters[task.priority] += 1
    # return render(request,"tasks/index.html", {'categories': categories, 'priorities':dict(priority_counters)})


    return render(request,"tasks/index.html", {'categories': categories, 'priorities': priorities, 'user': user, })



def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []    # Что это? Зачем это?
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        # tags = []
        categories = []

        for t in user_tasks:
            for cat in t.category.all():
                if cat not in categories:
                    categories.append(cat)
        context["categories"] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"


def get_time():
    return datetime.now().strftime("%A, %d. %B %Y %H:%M:%S")

def get_cached_time():
    if not cache.get('cached_time'):
        cache.set('cached_time', datetime.now().strftime("%A, %d. %B %Y %H:%M:%S"), 300)
    return cache.get('cached_time')

class CachedTimeView(View):
    template = "tasks/timenow.html"

    def get(self, request):
        context = {}
        context['timenow'] = get_time()
        context['cachedtime'] = get_cached_time()
        return render(request, self.template, context=context)

@cache_page(300)
def cashed_time_page(request):
    return render(
        request,
        "tasks/django_cached_page_timenow.html",
        {'cachedtime': get_time(),},
    )