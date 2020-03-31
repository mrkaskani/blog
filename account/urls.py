from django.urls import path, reverse_lazy
from .views import register, update_profile, success_change
from django.contrib.auth.views import (LoginView, LogoutView, logout_then_login, PasswordChangeView,
                                       PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView,
                                       PasswordResetCompleteView, PasswordResetConfirmView)

app_name = 'account'

urlpatterns = [
    # login
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='user_logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),
    # password change
    path('password_change/', PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')),
         name="password_change"),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
    # password reset
    path('password_reset', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>', PasswordResetConfirmView, name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # register
    path('register/', register, name='register'),
    path('edit/', update_profile, name='edit'),
    path('success', success_change, name='success')
]
