from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name = 'profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name = 'reset'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('confrim/<uidb64>/<token>/', views.PasswordResetConfrimView.as_view(), name = 'password_reset_confirm'),
    path('confrim/compelete', views.PasswordResetCompeleteView.as_view(), name = 'password_reset_complete'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name = 'follow'),
    path('unfollow/<int:user_id>/', views.UnfollowView.as_view(), name = 'unfollow'),
]
