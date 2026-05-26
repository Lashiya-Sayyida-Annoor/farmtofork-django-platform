from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
from MainProject.settings import *
from datetime import datetime






# Create your views here.
def FarmerHomepage(request):
    farmer = db.collection("tbl_farmer").document(request.session["fid"]).get().to_dict()
    return render(request, "Farmer/FarmerHomepage.html", {"farmer":farmer})    

def Profile(request):
    farmer = db.collection("tbl_farmer").document(request.session["fid"]).get().to_dict()
    print(farmer)
    return render(request, "Farmer/Profile.html", {"farmer":farmer})

def EditProfile(request):
    farmer = db.collection("tbl_farmer").document(request.session["fid"]).get().to_dict()
    if request.method =="POST":
        photo=request.FILES.get("file_photo")
        if photo:
            path="Farmer/Farmer_photo/"+photo.name
            sd.child(path).put(photo)
            d_url=sd.child(path).get_url(None)
            db.collection("tbl_Farmer").document(request.session["fid"]).update({"farmer_photo": d_url})

        db.collection("tbl_farmer").document(request.session["fid"]).update({"farmer_name":request.POST.get("txtname"),
       "farmer_contact":request.POST.get("txtcontact") })
        return redirect("webFarmer:Profile")
    else:
        return render(request,"Farmer/EditProfile.html",{"farmer":farmer})

def changepass(request):
    farmer = db.collection("tbl_farmer").document(request.session["fid"]).get().to_dict()
    email = farmer["farmer_email"]
        # print(email)
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
            'Reset your password ', #subject
            "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
    return redirect("webfarmer:Profile")

def vegetable(request):
    cat= db.collection("tbl_category").stream()
    cat_data = []
    for c in cat:
        data=c.to_dict()
        cat_data.append({"cat":data,"id":c.id}) 
        
    vegetable = db.collection("tbl_vegetable").stream()
    vegetable_data = []
    for v in vegetable:
        vegetable =v.to_dict()
        category= db.collection("tbl_category").document(vegetable["category_id"]).get().to_dict()
        vegetable_data.append({"vegetable":vegetable,"id":v.id,"cat_name":category})

    if request.method == "POST":
        Images = request.FILES.get("file_img")
        if Images:
            path = "Farmer/Farmer_photo/" + Images.name
            sd.child(path).put(Images)
            img_url = sd.child(path).get_url(None)
       
        db.collection("tbl_vegetable").add({
            "vegetable_name": request.POST.get('txtname'),
            "vegetable_price": request.POST.get('txtprice'),
            "category_id":request.POST.get('selcategory'),
            "vegetable_stock":request.POST.get('txtstock'),
            "vegetable_photo":img_url,  
            "farmer_id":request.session['fid'] 
        })

        return render(request,"Farmer/Vegetables.html")
    else:
        return render(request,"Farmer/Vegetables.html",{"category":cat_data,"data":vegetable_data})


def vegstock(request,vegid):
    veg = db.collection("tbl_vegetable").document(vegid).get().to_dict()
    oldstock = veg["vegetable_stock"]
    if request.method == "POST":
        total = int(oldstock) + int(request.POST.get("txtnstock"))
        db.collection("tbl_vegetable").document(vegid).update({"vegetable_stock":str(total)})
        return render(request,"Farmer/Vegetables.html",{"msg":"Stock updated.."})
    else:
        return render(request,"Farmer/VegStock.html")


def FarmerComplaints(request):
    id=request.session["fid"]

    compdata=db.collection("tbl_complaints").where("farmer_id", "==", request.session["fid"]).stream()
    complist=[]
    for i in compdata:
        comp=i.to_dict()
        complist.append({"comp_data":comp,"id":i.id})
        
    if request.method=="POST":
        data={"complaint_title":request.POST.get("txtctitle")
            ,"complaint_content":request.POST.get("txtccontent"),"farmer_id":id,"uid":0}
        db.collection("tbl_complaints").add(data)
        return redirect("webFarmer:FarmerComplaints")
    else:
        return render(request,"Farmer/FarmerComplaints.html",{"data":complist})        

def farmerfeedback(request):
    id=request.session["fid"]
    if request.method=="POST":
        data={"feedback_content":request.POST.get("txtfcontent")
            ,"farmer_id":id,"uid":0,"feedback_time":datetime.now()}
        db.collection("tbl_feedbacks").add(data)
        return redirect("webFarmer:farmerfeedback")
    else:
        return render(request,"Farmer/FarmerFeedback.html")

def viewbooking(request):
    comp = booking.to_dict()
    cdata = db.collection("tbl_cart").where("booking_id", "==", booking.id).stream()
    for booking in compdata:
        comp = booking.to_dict()
        cdata = db.collection("tbl_cart").where("booking_id", "==", booking.id).stream()
    complist.append({"data": booking.to_dict(), "id": booking.id})
    return render(request, "User/ViewBooking.html",{"complist":complist})

    
   