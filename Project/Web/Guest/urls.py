from django.urls import path
from Guest import views

app_name = "webGuest"

urlpatterns = [
    
    path('userreg/', views.userreg,name="UserReg"),
    path('ajax_place/', views.ajax_place,name="ajaxplace"),
    path('login/', views.login,name="login"),
    path('farmerreg/', views.farmerreg,name="farmerreg"),
    path('index/', views.index,name="index"),


   ]       