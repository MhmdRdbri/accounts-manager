from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    path("users/register/", CustomUserCreateView.as_view(), name="user-register"),
    path("users/login/", UserLoginView.as_view(), name="user-login"),
    path("admin/users/", AdminUserListView.as_view(), name="admin-user-list"),
    path(
        "admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"
    ),
    path("user/profile/edit/", UserProfileEditView.as_view(), name="user-profile-edit"),
]
