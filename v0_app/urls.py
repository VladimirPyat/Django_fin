from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('recipe_add/', views.recipe_add, name='recipe_add'),
    path('recipe_show/<int:pk>', views.recipe_show, name='recipe_show'),
    path('', views.main_page, name='main_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)