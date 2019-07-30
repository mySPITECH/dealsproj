from . import views
from django.conf.urls import url
from django.urls import path

app_name = 'View'
urlpatterns = [
    path('',views.home,name='home'),
url(r'^index',views.home,name='index'),
path('login/',views.login2,name='login'),
path('logout/',views.log_uerout,name='logout'),
    path('welcome/<str:token>', views.verifyAccount),
    path('signup/',views.create_account,name='signup2'),
    path('login/',views.verification_login,name='login_uri'),
    url(r'^profile/',views.user_profile,name='myprofile'),
    path('save_deal',views.save_deal,name='create_deal'),
    path('clear_deal/<str:token>',views.deal_clearance,name='clear_deal'),
    path('clearance/',views.save_clearance,name="verify_deal"),
    path('listing/<int:pk>',views.deal_deail,name="deal-details"),
    url(r'^signup',views.sign_up,name='sign-up'),
    path('save_form/',views.registar,name='registar'),
        path('mydeals/',views.user_deals,name='mydeal'),
    url(r'^request-deal/',views.deal_process,name="request_deal"),
        url(r'^dashboard/',views.dashboard,name="dashboard"),




    
]
