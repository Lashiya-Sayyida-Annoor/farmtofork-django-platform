from django.urls import path
from User import views

app_name="webuser"

urlpatterns = [

path('UserHomepage/', views.UserHomepage,name="UserHomepage"),
path('Profile/',views.Profile,name="Profile"),
path('EditProfile/',views.EditProfile,name="EditProfile"),
path('changepass/',views.changepass,name="changepass"),
path('searchveg/<str:id>',views.searchveg,name="searchveg"),
path('UserComplaints/',views.UserComplaints,name="UserComplaints"),
path('searchfarmer/',views.searchfarmer,name="searchfarmer"),
path('ajaxfarmer/',views.ajaxfarmer,name="ajaxfarmer"),
path('ajaxvegetable/',views.ajaxvegetable,name="ajaxvegetable"),
path('ajaxvegetablekeysearch/',views.ajaxvegetablekeysearch,name="ajaxvegetablekeysearch"),
path('vegetablecart/<str:pid>',views.vegetablecart,name="vegetablecart"),
path('userfeedback/',views.userfeedback,name="userfeedback"),
path('mybooking/',views.mybooking,name="mybooking"),
path('myproduct/<str:id>',views.myproduct,name="myproduct"),
path('bills/<str:id>',views.bills,name="bills"),
path('rating/<str:id>',views.rating,name="rating"),
path('ajaxrating',views.ajaxrating,name="ajaxrating"),
path('starrating/',views.starrating,name="starrating"),





path('searchpro/',views.searchpro,name="searchpro"),

path('mycart/',views.mycart,name="mycart"),
path('deletecartitem/<str:cid>',views.deletecartitem,name="deletecartitem"),
path('ajaxmycart/',views.ajaxmycart,name="ajaxmycart"),

path('payment/',views.payment,name="payment"),
path('loader/',views.loader,name="loader"),
path('paymentsuc/',views.paymentsuc,name="paymentsuc"),



]

