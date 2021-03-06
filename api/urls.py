from django.urls import path

from api import views

urlpatterns = [
    path('book/', views.BookAPIView.as_view()),
    path('book/<str:id>/', views.BookAPIView.as_view()),
    path('user/login/', views.UserAPIView.as_view({"post": "user_login"})),
    path('user/register/', views.UserAPIView.as_view({"post": "user_register"})),
]
