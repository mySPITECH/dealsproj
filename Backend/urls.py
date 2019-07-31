from . import views
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name='Backend'
urlpatterns = [
    path('web-manager/',views.index,name="web-master"),
    path('manage-user/', views.manage_user,name="user-manager"),
    path('user-detail/<int:pk>', views.user_detail,name="details"),
    path('deal_request/<str:token>',views.save_deal,name="save-deal"),
        path('my_request/',views.save_deals,name="my-request"),
path('user_admin/',views.user_manage,name='user-admin'),
     path('deal_detail/<int:pk>',views.deal_details,name="deal-detail"),
    path('dealstatus/',views.deal_status,name="dealstatus"),
 path('request_record/',views.deal_record,name="request-record"),
  path('request_moderation/<str:code>',views.deal_moderation,name="deal_moderation"),
    path('request_moderation/',views.approve_request,name="reqstatus"),
        path('user_record/',views.users_record,name="user-record"),
            path('user_detail<int:pk>/',views.user_detail,name="user-detail"),
                path('settings/',views.settings,name="settings"),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
