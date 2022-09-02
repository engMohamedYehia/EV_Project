
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('logoutuser/', views.logout_user, name='logout_user'),
    path('main/', views.main_page, name='main_page'),

    path('group/',views.group_page,name='group_page'),
    path('creategroup/',views.create_group_page,name='create_group_page'),
    path('updategroup/<str:pk>',views.update_group_page,name='update_group_page'),
    path('deletegroup/<str:pk>',views.delete_group_page,name='delete_group_page'),
    path('viewgroup/<str:pk>',views.view_group_page,name='view_group_page'),
    

    path('report/',views.report_page,name='report_page'),
    path('createreport/',views.create_report_page,name='create_report_page'),
    path('updatereport/<str:pk>',views.update_report_page,name='update_report_page'),
    path('deletereport/<str:pk>',views.delete_report_page,name='delete_report_page'),
    path('viewreport/<str:pk>',views.view_report_page,name='view_report_page'),
    

    path('usermanagment/',views.usermanagment_page,name='usermanagment_page'),
    path('createusermanagment/',views.create_usermanagment_page,name='create_usermanagment_page'),
    path('updateusermanagment/<str:pk>',views.update_usermanagment_page,name='update_usermanagment_page'),
    path('deleteusermanagment/<str:pk>',views.delete_usermanagment_page,name='delete_usermanagment_page'),
    path('viewuser/<str:pk>',views.view_user_page,name='view_user_page'),

    path('role/',views.role_page,name='role_page'),

]


urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
