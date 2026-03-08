from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.admin_page, name='portfolio_admin'),
    path('dashboard/messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('dashboard/messages/<int:message_id>/mark-read/', views.mark_message_read, name='mark_message_read'),
]
