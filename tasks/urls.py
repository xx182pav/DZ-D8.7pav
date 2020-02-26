from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.TaskListView.as_view(), name="list"),
    path("list/c/<slug:cat_slug>", views.tasks_by_cat, name="list_by_cat"),
    path("details/<int:pk>", views.TaskDetailsView.as_view(), name="details"),
    path('cached-time/', views.CachedTimeView.as_view(), name='cached_time_url'),
    path("cachedpage-time/", views.cashed_time_page, name="cashed_page_time_url"),
]