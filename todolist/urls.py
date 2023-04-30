from django.urls import path
from todolist import views

urlpatterns = [
    path('', views.TodolistView.as_view(), name= 'todolist_view'),
    path('<int:todolist_id>/', views.TodolistDetailView.as_view(), name='todolist_detail_view'),
]
