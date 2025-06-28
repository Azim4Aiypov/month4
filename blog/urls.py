"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts.views import homepage_view, test_view, posts_list_view 
from users.views import register_view, login_view, logout_view
from django.conf.urls.static import static
from django.conf import settings
from users import views as user_views
from posts import views  # ✅ добавлен импорт для доступа к views.post_detail_view и post_create_view

users_urls = [
    path('register/', user_views.register_view, name='register_view'),
    path('login/', user_views.login_view, name='login_view'),
    path('logout/', user_views.logout_view, name='logout_view'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name='home_view'),
    path('test/', test_view, name='test_view'),
    path('posts/', posts_list_view, name='posts_list_view'),
    path('posts/<int:post_id>/', views.post_detail_view, name='post_detail_view'),
    path('posts/create/', views.post_create_view, name='post_create_view'),
] 
urlpatterns += users_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)