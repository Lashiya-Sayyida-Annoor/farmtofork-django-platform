from django.urls import path
from Admin import views

app_name="webadmin"


urlpatterns = [
    
    path('adminprofile/', views.adminprofile,name="adminprofile"),
    path('editaprofile/', views.edit_admin,name="editaprofile"),
    path('Homepage/', views.Homepage,name="Homepage"),
    path('district/', views.district,name="district"),
    path('category/', views.category,name="category"),
    path('adminreg/',views.adminregistration,name="adminreg"),
    path('delete_dis/<str:delid>',views.delete_dis,name="delete_dis"),
    path('edit_dis/<str:editid>',views.edit_dis,name="edit_dis"),
    path('delete_cat/<str:delcatid>',views.delete_cat,name="delete_cat"),
    path('edit_cat/<str:editcatid>',views.edit_cat,name="edit_cat"),
    path('place/', views.place,name="place"),
    path('subcategory/',views.subcategory,name="subcategory"),
    path('delete_place/<str:placeid>',views.delete_place,name="delete_place"),
    path('edit_place/<str:plaid>',views.edit_place,name="edit_place"),
    path('delete_subcat/<str:subcatid>',views.delete_subcat,name="delete_subcat"),
    path('verifyfarmer/',views.verifyfarmer,name="verifyfarmer"),
    path('reject_farmer/<str:rejid>',views.reject_farmer,name="reject_farmer"),
    path('accept_farmer/<str:accid>',views.accept_farmer,name="accept_farmer"),


    path('categoryreport/',views.categoryreport,name="categoryreport"),


    path('viewcomplaints/',views.viewcomplaints,name="viewcomplaints"),
    path('replycomplaints/<str:id>',views.replycomplaints,name="replycomplaints"),
    path('viewfeedbacks/',views.viewfeedbacks,name="viewfeedbacks"),

    path('report/',views.report,name="report"),






    
]


