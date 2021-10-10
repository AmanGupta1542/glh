from django.urls import path
from users import views
urlpatterns = [
    path('signup/', views.signup ,name='signup'),

    path('signout/', views.signout ,name='signout'),

    path('signin/', views.signin,name='signin'),

    path('signin-submit/', views.signin_submit,name='signin-submit'),

    path('signup-submit/', views.signup_submit,name='signup-submit'),

    path('forget-password/', views.forget_password,name='forget-password'),
    
    path('password-recover/<int:userid>', views.password_recover,name='password-recover'),

    path('rocovery-template/<token>/', views.rocovery_template, name="reset_password"),

    path('forget-password-submit/', views.forget_password_submit,name='forget-password-submit'),

    path('settings/', views.settings ,name='settings'),

    path('settings-edit/', views.settings_edit ,name='settings-edit'),

    path('settings-submit/<int:userid>/', views.settings_submit ,name='settings-submit'),
]
