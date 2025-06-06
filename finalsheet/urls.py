from django.urls import path
from .import views
urlpatterns = [
    path('superuser/UserRegister/', views.signup_view, name='signup'),
    path('user/login/', views.login_view, name='loginu'),
    path('superuser/login/', views.login1_view, name='login'),
    path('BOM/', views.add_bom, name='BOMP'),
    path('BOM1/',views.add_bom1,name='upload1'),
    path('BOMt/',views.add_bom3,name='BOM1'),
    path('home/', views.button_page, name='home'),
    path('superuser/services/', views.admin_page, name='superuser'),
    path('logout/', views.logout_view, name='logout_view'),
    path('user-activity/', views.user_activity_view, name='user_activity'),
    path('user/services/', views.user_page, name='user'),
    path('user-activity/<int:activity_id>/', views.view_downloaded_pdf, name='view_downloaded_pdf'),
]