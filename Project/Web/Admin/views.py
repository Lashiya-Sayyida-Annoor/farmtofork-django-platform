from django.shortcuts import render,redirect
from Admin.models import *
from MainProject.settings import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
import json



# Create your views here.
def district(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        data = {"dis":d.to_dict(),"id":d.id}
        dis_data.append(data)
        # dis_data.append({"dis":d.to_dict(),"id":d.id})
    if request.method=="POST": 
        db.collection("tbl_district").add({"district_name":request.POST.get('txtdist')})
        return render(request,"Admin/District.html")
    else:
        return render(request,"Admin/District.html",{"district":dis_data})

def delete_dis(request,delid):
    db.collection("tbl_district").document(delid).delete()
    return redirect("webadmin:district")

def edit_dis(request,editid):
    dis = db.collection("tbl_district").document(editid).get().to_dict()
    if request.method == "POST":
        dist = request.POST.get('txtdist')
        dis_dict = {"district_name":dist}
        db.collection("tbl_district").document(editid).update(dis_dict)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"disdata":dis})


def category(request):
    cat = db.collection("tbl_category").stream()
    cat_data = []
    for d in cat:
        data = {"cat":d.to_dict(),"id":d.id}
        cat_data.append(data)

    if request.method=="POST":
        db.collection("tbl_category").add({"category_name":request.POST.get('txtcat')})
        return render(request,"Admin/Category.html")
    else:
        return render(request,"Admin/Category.html",{"category":cat_data})

def delete_cat(request,delcatid):
    db.collection("tbl_category").document(delcatid).delete()
    return redirect("webadmin:category")

def edit_cat(request,editcatid):
    cat = db.collection("tbl_category").document(editcatid).get().to_dict()
    if request.method == "POST":
        cati = request.POST.get('txtcat')
        cat_dict = {"category_name":cati}
        db.collection("tbl_category").document(editcatid).update(cat_dict)
        return redirect("webadmin:category")
    else:
        return render(request,"Admin/Category.html",{"catdata":cat})



def adminregistration(request):
    
    if request.method=="POST":
        email = request.POST.get("txtemail")
        password = request.POST.get("txtpass")
        try:
            admin = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Admin/Adminregistration.html",{"msg":error})
        Images = request.FILES.get("file_photo")
        if Images is not None:
            path = "Admin/Admin_photo/" + Images.name
            sd.child(path).put(Images)
            img_url = sd.child(path).get_url(None)

            

        
        db.collection("tbl_adminregistration").add({
            "admin_id":admin.uid,
            "admin_name": request.POST.get('txtname'),
            "admin_contact": request.POST.get('txtcontact'),
            "admin_email": request.POST.get('txtemail'),
            "admin_photo":img_url,
         })
        return render(request, "Admin/AdminRegistration.html")
    else:
        return render(request, "Admin/AdminRegistration.html")

def edit_admin(request):
    admin = db.collection("tbl_adminregistration").document(request.session["aid"]).get().to_dict()    
    if request.method =="POST":

        photo=request.FILES.get("file_photo")
        if photo:
            path="Admin/Admin_photo/"+photo.name
            sd.child(path).put(photo)
            d_url=sd.child(path).get_url(None)
            db.collection("tbl_adminregistration").document(request.session["aid"]).update({"admin_photo": d_url})

        db.collection("tbl_adminregistration").document(request.session["aid"]).update({"admin_name":request.POST.get("txtname"),
       "admin_contact":request.POST.get("txtcontact") })
        return redirect("webadmin:adminprofile")
    else:
        return render(request,"Admin/EditProfile.html",{"admin":admin})

def place(request):
    dis= db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        data=d.to_dict()
        dis_data.append({"dis":data,"id":d.id}) 
        
    place = db.collection("tbl_place").stream()
    place_data = []
    for p in place:
        place =p.to_dict()
        district=db.collection("tbl_district").document(place["district_id"]).get().to_dict()
        place_data.append({"place":place,"id":p.id,"dis_name":district})
    

    if request.method == "POST":
       
        db.collection("tbl_place").add({
            "place_name": request.POST.get('txtplace'),
            "place_pincode": request.POST.get('txtpin'),
            "district_id":request.POST.get('seldistrict')
           
        })

        return render(request, "Admin/Place.html")
    else:
        return render(request, "Admin/Place.html",{"district":dis_data,"data":place_data})


def delete_place(request,placeid):
    db.collection("tbl_place").document(placeid).delete()
    return redirect("webadmin:place")

def edit_place(request,plaid):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        data =d.to_dict()
        dis_data.append({"dis":data,"id":d.id})
    place=db.collection("tbl_place").document(plaid).get().to_dict()

    if request.method == "POST":
        db.collection("tbl_place").document(plaid).update({"place_name":request.POST.get("txtplace"),
        "place_pincode":request.POST.get("txtpin"),"district_id":request.POST.get("seldistrict")})
        return redirect("webadmin:place")
    else:
        return render(request,"Admin/Place.html",{'district':dis_data,'place_data':place})

def subcategory(request):
    subcatta=tbl_subcategory.objects.all()
    subcatdata=tbl_category.objects.all() 
    if request.method=="POST":
        subid=tbl_category.objects.get(id=request.POST.get('cat_list'))       
        tbl_subcategory.objects.create(
            subcategory_name=request.POST.get('txtsubcat'),
            category=subid
            )
        db.collection("tbl_subcategory").add({
            "subcategory_name":request.POST.get('txtsubcat'),
            "category":subid.id 
        })
        return render(request,"Admin/SubCategory.html",{'subdata':subcatdata})
    else:
        return render(request,"Admin/SubCategory.html",{'subdata':subcatdata,"ssub":subcatta})


def delete_subcat(request,subcatid):
    tbl_subcategory.objects.get(id=subcatid).delete()
    return redirect("webadmin:subcategory")

def Homepage(request):
    admin = db.collection("tbl_adminregistration").document(request.session["aid"]).get().to_dict()
    return render(request, "Admin/Homepage.html" , {"admin":admin})    

def adminprofile(request):
    admin = db.collection("tbl_adminregistration").document(request.session["aid"]).get().to_dict()
    return render(request, "Admin/Profile.html", {"admin":admin})


def verifyfarmer(request):
    farmer=db.collection("tbl_farmer").stream()
    pdata =[]
    for p in farmer:
        pdata.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Admin/VerifyFarmer.html",{"pdata":pdata})

def reject_farmer(request,rejid):
    db.collection("tbl_farmer").document(rejid).delete()
    return redirect("webadmin:verifyfarmer")      

def accept_farmer(request,accid):
    db.collection("tbl_farmer").document(accid).update({"fam_status": 1})
    farmer = db.collection("tbl_farmer").document(accid).get().to_dict() 
    email = farmer['farmer_email']
    send_mail(
        'Welcome to FarmToFork !',
        'Dear ' + farmer['farmer_name'] + ',\n\n'
        'We are excited to welcome you to farmToFork. Your farmer status has been accepted!\n\n'
        'Thank you for choosing farmToFork. If you have any questions or need assistance, feel free to reach out.\n\n'
        'Best regards,\n'
        'The FarmToFork Team',
        
        settings.EMAIL_HOST_USER,
        [email],
    )                                
    return redirect("webadmin:verifyfarmer")
def viewcomplaints(request):
    ccompdata = db.collection("tbl_complaints").where("farmer_id", "!=", 0).stream()
    ccomplist = []
    for i in ccompdata:
        comp = i.to_dict()
        farmer_doc = db.collection("tbl_farmer").document(comp["farmer_id"]).get()
        if farmer_doc.exists:
            farmer_data = farmer_doc.to_dict()
            ccomplist.append({"ccomp_data": comp, "id": i.id, "farmer": farmer_data})

    ccompdata = db.collection("tbl_complaints").where("uid", "!=", 0).stream()
    ccomplist2 = []
    for i in ccompdata:
        comp = i.to_dict()
        user_doc = db.collection("tbl_user").document(comp["uid"]).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            ccomplist2.append({"ccomp_data": comp, "id": i.id, "user": user_data})

    return render(request, "Admin/ViewComplaints.html", {"data": ccomplist, "data2": ccomplist2})

def replycomplaints(request,id):
    if request.method=="POST":
        db.collection("tbl_complaints").document(id).update({"complaint_reply":request.POST.get("txtreply")})
        return redirect("webadmin:viewcomplaints")
    else:
        return render(request,"Admin/ReplyComplaints.html")

def viewfeedbacks(request):
    feeddata=db.collection("tbl_feedbacks").where("farmer_id","!=",0).stream()
    feedlist1=[]
    for i in feeddata:
        feed=i.to_dict()
        center=db.collection("tbl_farmer").document(feed["farmer_id"]).get().to_dict()
        feedlist1.append({"cfeed_data":feed,"id":i.id,"center":center})

    feeddata=db.collection("tbl_feedbacks").where("uid","!=",0).stream()
    feedlist2=[]
    for i in feeddata:
        feed=i.to_dict()
        user=db.collection("tbl_user").document(feed["uid"]).get().to_dict()
        feedlist2.append({"ufeed_data":feed,"id":i.id,"user":user})
    return render(request,"Admin/ViewFeedback.html",{"data":feedlist1,"data2":feedlist2})



    
def categoryreport(request):    
    bookids = []
    catlist = []
    xlist=[]
    ylist=[]
    cdata = db.collection("tbl_category").stream()     
    for c in cdata:
        category = c.to_dict()
        sdata = db.collection("tbl_vegetable").where("category_id", "==", c.id).stream()
        for s in sdata:
            subcategory = s.to_dict()
            codata = db.collection("tbl_cart").where("vegetable_id", "==", s.id).where('cart_status', '==', ).stream()
            for co in codata:
                book = b.to_dict()
                bookids.append(b.id)
        count = len(bookids)
        #cat = 
        catlist.append({"catname": category['category_name'],"count":count})
        bookids=[]
        # print("data:",catlist)
    for i in catlist:
        
        xlist.append(i['catname'])   
        ylist.append(i['count'])
    x_json = json.dumps(xlist)
    y_json = json.dumps(ylist)
    print("xx:",xlist)
    print("yy:",ylist)         
    return render(request, "Admin/CategoryReport.html", {"x": x_json,"y":y_json})

def report(request):
    cart = db.collection("tbl_cart").stream()
    cart_data = []
    for i in cart:
        cart_data.append({"cart"})
    return render(request,"Admin/Report.html")