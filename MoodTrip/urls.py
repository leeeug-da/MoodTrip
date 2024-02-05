"""
URL configuration for MoodTrip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# MoodTrip/urls.py
from django.contrib import admin
from django.urls import path, include  
from Moodmatcher import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main'),
    path('service-intro/', views.service_intro, name='service_intro'),
    path('recommend/', views.recommend_view, name='recommend'),
    path('recommend/image-choice/', views.image_choice_recommend, name='image_choice_recommend'),
    path('recommend/image-upload/', views.image_upload_recommend, name='image_upload_recommend'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('community/', include('Moodmatcher.urls')),  # Moodmatcher 앱의 URL을 include
    path('customer-service/', views.customer_service, name='customer_service'),
    path('<str:category>/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout'),  # 'main'으로 리다이렉트
    path('Moodmatcher/', include('Moodmatcher.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
