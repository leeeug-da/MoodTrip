from django.urls import path
from . import views
from .views import image_upload_recommend
from .views import my_profile
from .views import post_like
from .views import random_image
from .views import upload_image
from .views import recommend_tourist_spots_from_images
from .views import show_selected_spot


urlpatterns = [
    path('tour_category/', views.tour_category, name='tour_category'),
    path('community/', views.community, name='community'),
    path('customer-service/', views.customer_service, name='customer_service'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),
    path('<str:category>/post/create/community/', views.post_create, name='post_create'),
    path('<str:category>/post/create/customer-service/', views.post_create_customer_service, name='post_create_customer_service'),
    path('<str:category>/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('<str:category>/post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('<str:category>/post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('<str:category>/post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('image_upload_recommend/', image_upload_recommend, name='image_upload_recommend'),
    path('upload_image/', views.upload_image, name='upload_image'),  # 이 라인을 추가하세요
    path('my_profile/', my_profile, name='my_profile'),
    path('image_choice_recommend/result/', views.image_choice_recommend_result, name='image_choice_recommend_result'),
    path('image_upload_recommend/result/', views.image_upload_recommend_result, name='image_upload_recommend_result'),
    path('random_image/', random_image, name='random_image'),
    path('upload_image/', upload_image, name='upload_image'),
    path('recommend-tourist-spots/', recommend_tourist_spots_from_images, name='recommend_tourist_spots'),
    path('show-selected-spot/<int:selected_index>/', views.show_selected_spot, name='show_selected_spot'),
]
