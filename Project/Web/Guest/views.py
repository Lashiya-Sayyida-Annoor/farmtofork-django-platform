from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
from MainProject.settings import *
from datetime import datetime

# Create your views here.
def userreg(request):
    
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
            data =d.to_dict()
            dis_data.append({"dis":data,"id":d.id})
    if request.method=="POST":
        email = request.POST.get("txtemail")
        password = request.POST.get("txtpass")
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/UserRegistration.html",{"msg":error})
        Images = request.FILES.get("file_photo")
        if Images:
            path = "User/User_photo/" + Images.name
            sd.child(path).put(Images)
            img_url = sd.child(path).get_url(None)
            # print(img_url)
        
        
        db.collection("tbl_user").add({"name":request.POST.get('txtname'),
           "contact":request.POST.get('txtcontact'),
            "email":request.POST.get('txtemail'),
            "gender":request.POST.get('btngender'),
            "address":request.POST.get('txtarea'),
            "uid":user.uid,
            "dob":request.POST.get('txtdob'),
            "image":img_url,
            #"user_proof":request.FILES.get('file_proof'),

            "password":request.POST.get('txtpass'),
        })
        return render(request,"Guest/UserRegistration.html")
    else:
        return render(request,"Guest/UserRegistration.html",{'district':dis_data})


def farmerreg(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
            data =d.to_dict()
            dis_data.append({"dis":data,"id":d.id})
    if request.method=="POST":
        email = request.POST.get("txtemail")
        password = request.POST.get("txtpass")
        try:
            farmer = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/FarmerRegistration.html",{"msg":error})
        Images = request.FILES.get("file_photo")
        if Images:
            path = "Farmer/Farmer_photo/" + Images.name
            sd.child(path).put(Images)
            img_url = sd.child(path).get_url(None)
            # print(img_url)
        
        
        db.collection("tbl_farmer").add({"farmer_name":request.POST.get('txtname'),
           "farmer_contact":request.POST.get('txtcontact'),
            "farmer_email":request.POST.get('txtemail'),
            "farmer_address":request.POST.get('txtarea'),
            "farmer_id":farmer.uid,
            "farmer_photo":img_url,
            "fam_status":0,
            "place_id":request.POST.get('sel_place'),
            #"user_proof":request.FILES.get('file_proof'),

            "farmer_password":request.POST.get('txtpass'),
        })
        return render(request,"Guest/FarmerRegistration.html")
    else:
        return render(request,"Guest/FarmerRegistration.html",{'district':dis_data})



def ajax_place(request):
    place=db.collection("tbl_place").where("district_id", "==", request.GET.get('did')).stream()
    pla_data = []
    for p in place:
        pla_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"pdata":pla_data})



def login(request):
    
    adminid=""
    userid=""
    farmerid=""
    if request.method=="POST":        
        email=request.POST.get("txtemail")
        password=request.POST.get("txtpass")
        try:
            data=authe.sign_in_with_email_and_password(email,password)
        except:
            return render(request,"Guest/Login.html",{"msg":"Email and password Error"})
        ids=data["localId"]
        admin=db.collection("tbl_adminregistration").where("admin_id","==",ids).stream()
        for a in admin:
            adminid= a.id
        user=db.collection("tbl_user").where("uid","==",ids).stream()
        for u in user:
            userid= u.id
        farmer=db.collection("tbl_farmer").where("farmer_id","==",ids).stream()
        for f in farmer:
            farmerid= f.id

        if adminid:
            request.session["aid"]=adminid
            return redirect("webadmin:Homepage")
        elif userid:
            request.session["uid"]=userid
            return redirect("webuser:UserHomepage")
        elif farmerid:
            request.session["fid"]=farmerid
            return redirect("webFarmer:FarmerHomepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Error"})
        
    else:
        return render(request,"Guest/Login.html")


    

def index(request):
    return render(request,"Guest/index.html")