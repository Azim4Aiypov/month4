from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from posts.views import homepage_view, test_view, posts_list_view
from posts import views as post_views  
from users import views as user_views

users_urls = [
    path('register/', user_views.register_view, name='register_view'),
    path('login/', user_views.login_view, name='login_view'),
    path('logout/', user_views.logout_view, name='logout_view'),
    path('profile/', user_views.profile_view, name='profile_view'),  # ✅ ДОБАВИЛИ ЭТУ СТРОКУ
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name='home_view'),
    path('test/', test_view, name='test_view'),
    path('posts/', posts_list_view, name='posts_list_view'),
    path('posts/<int:post_id>/', post_views.post_detail_view, name='post_detail_view'),
    path('posts/create/', post_views.post_create_view, name='post_create_view'),

    # Редирект с /accounts/login/ на /login/
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
]

urlpatterns += users_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
