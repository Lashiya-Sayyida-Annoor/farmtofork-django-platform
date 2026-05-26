from django.urls import path
from Farmer import views

app_name = "webFarmer"

urlpatterns = [
path('FarmerHomepage/', views.FarmerHomepage,name="FarmerHomepage"),
path('Profile/',views.Profile,name="Profile"),
path('EditProfile/',views.EditProfile,name="EditProfile"),
path('changepass/',views.changepass,name="changepass"),
path('vegetable/',views.vegetable,name="vegetable"),
path('vegstock/<str:vegid>',views.vegstock,name="vegstock"),
path('FarmerComplaints/',views.FarmerComplaints,name="FarmerComplaints"),
path('farmerfeedback/',views.farmerfeedback,name="farmerfeedback"),
path('viewbooking/',views.viewbooking,name="viewbooking"),







]       