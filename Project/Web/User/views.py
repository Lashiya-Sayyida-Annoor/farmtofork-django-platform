from django.shortcuts import render,redirect
from Admin.models import *
from MainProject.settings import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date
import random

# Create your views here.

def UserHomepage(request):

    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    return render(request, "User/UserHomepage.html", {"user":user})

def Profile(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    print(user)
    return render(request, "User/Profile.html", {"user":user})

def EditProfile(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    if request.method =="POST":

        photo=request.FILES.get("file_photo")
        if photo:
            path="User/image/"+photo.name
            sd.child(path).put(photo)
            d_url=sd.child(path).get_url(None)
            db.collection("tbl_user").document(request.session["uid"]).update({"image": d_url})

        db.collection("tbl_user").document(request.session["uid"]).update({"name":request.POST.get("txtname"),
       "contact":request.POST.get("txtcontact") })
        return redirect("webuser:Profile")
    else:
        return render(request,"User/EdiltProfile.html",{"user":user})


def changepass(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    email = user["email"]
        # print(email)
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
            'Reset your password ', #subject
            "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
    return redirect("webuser:Profile")

def searchveg(request,id):
    veg = db.collection("tbl_vegetable").where("farmer_id", "==", id).stream()
    veg_data = []
    for v in veg:
        vdata = v.to_dict()
        cat = db.collection("tbl_category").document(vdata["category_id"]).get().to_dict()
        veg_data.append({"vegetable":v.to_dict(),"id":v.id,"cat_name":cat})
    cat = db.collection("tbl_category").stream()
    cat_data = []
    for c in cat:
        cat_data.append({"category":c.to_dict(),"id":c.id})
    if request.method == "POST":
        search_query = request.POST.get("search_query", "").strip()

        # Query vegetables collection in Firestore based on search_query
        vegetables_ref = db.collection("tbl_vegetables")
        query = vegetables_ref.where("vegetable_name", "==", search_query).get()

        # Process query results
        search_results = []
        for doc in query:
            vegetable_data = doc.to_dict()
            search_results.append(vegetable_data)

        return render(request, "User/SearchVegetables.html", {"search_results": search_results})
    else:
        return render(request, "User/SearchVegetables.html",{"vegetable":veg_data,"category":cat_data})

def searchpro(request):
    veg = db.collection("tbl_vegetable").stream()
    veg_data = []
    for v in veg:
        vdata = v.to_dict()
        cat = db.collection("tbl_category").document(vdata["category_id"]).get().to_dict()
        veg_data.append({"vegetable":v.to_dict(),"id":v.id,"cat_name":cat})
    cat = db.collection("tbl_category").stream()
    cat_data = []
    for c in cat:
        cat_data.append({"category":c.to_dict(),"id":c.id})
    if request.method == "POST":
        search_query = request.POST.get("search_query", "").strip()

        # Query vegetables collection in Firestore based on search_query
        vegetables_ref = db.collection("tbl_vegetables")
        query = vegetables_ref.where("vegetable_name", "==", search_query).get()

        # Process query results
        search_results = []
        for doc in query:
            vegetable_data = doc.to_dict()
            search_results.append(vegetable_data)

        return render(request, "User/SearchProduct.html", {"search_results": search_results})
    else:
        return render(request, "User/SearchProduct.html",{"vegetable":veg_data,"category":cat_data})

def ajaxvegetable(request):
    veg = db.collection("tbl_vegetable").where("category_id", "==", request.GET.get("cid")).stream()
    veg_data = []
    for v in veg:
        vdata = v.to_dict()
        cat = db.collection("tbl_category").document(vdata["category_id"]).get().to_dict()
        veg_data.append({"vegetable":v.to_dict(),"id":v.id,"cat_name":cat})
    return render(request,"User/AjaxVegetable.html",{"vegetable":veg_data})

def ajaxvegetablekeysearch(request):
    veg = db.collection("tbl_vegetable").where("vegetable_name", ">=", request.GET.get("key").capitalize()).where('vegetable_name', '<=', request.GET.get("key").capitalize() + u'\uf8ff').stream()
    veg_data = []
    for v in veg:
        vdata = v.to_dict()
        cat = db.collection("tbl_category").document(vdata["category_id"]).get().to_dict()
        veg_data.append({"vegetable":v.to_dict(),"id":v.id,"cat_name":cat})
    return render(request,"User/AjaxVegetable.html",{"vegetable":veg_data})

def searchfarmer(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        dis_data.append({"district":d.to_dict(),"id":d.id}) 
    far = db.collection("tbl_farmer").stream()
    far_data = []
    for f in far:
        far_data.append({"farmer":f.to_dict(),"id":f.id}) 
    return render(request,"User/SearchFarmer.html",{"district":dis_data,"farmer":far_data})

def ajaxfarmer(request):
    if request.GET.get("pid")!="":
        far = db.collection("tbl_farmer").where("place_id", "==", request.GET.get("pid")).stream()
        far_data = []
        for f in far:
            far_data.append({"farmer":f.to_dict(),"id":f.id}) 
        return render(request,"User/AjaxFarmer.html",{"farmer":far_data})
    else:
        place = db.collection("tbl_place").where("district_id", "==",request.GET.get("did")).stream()
        far_data = []
        for p in place:
            far = db.collection("tbl_farmer").where("place_id", "==", p.id).stream()
            for f in far:
                far_data.append({"farmer":f.to_dict(),"id":f.id}) 
        return render(request,"User/AjaxFarmer.html",{"farmer":far_data})

def vegetablecart(request,pid):
    bid = ""
    bk = db.collection("tbl_booking").where("booking_status", "==", 0).where("user_id", "==", request.session["uid"]).get()
    if len(bk) > 0:
        for b in bk:
            bid = b.id
        cart = db.collection("tbl_cart").where("product_id", "==", pid).where("booking_id", "==", bid).get()
        if len(cart) > 0:
            return render(request,"User/SearchVegetables.html",{"msg":"Product Is Already Add To Cart"})
        else:
            db.collection("tbl_cart").add({"product_id":pid,"booking_id":bid,"cart_qty":1,"cart_status":0})
            return render(request,"User/SearchVegetables.html",{"msg":"Product Add To Cart"})
    else:
        db.collection("tbl_booking").add({"user_id":request.session["uid"],"booking_status":0,"booking_date":str(date.today())})
        booking = db.collection("tbl_booking").where("booking_status", "==", 0).where("user_id", "==", request.session["uid"]).get()
        if len(booking) > 0:
            for b in booking:
                bid = b.id
            db.collection("tbl_cart").add({"product_id":pid,"booking_id":bid,"cart_qty":1,"cart_status":0})
            return render(request,"User/SearchVegetables.html",{"msg":"Product Add To Cart"})
        else:
            return render(request,"User/SearchVegetables.html")

def mycart(request):
    bkid = ""
    booking = db.collection("tbl_booking").where("user_id", "==", request.session["uid"]).where("booking_status", "==", 0).stream()
    for b in booking:
        bkid = b.id
    cart = db.collection("tbl_cart").where("booking_id", "==", bkid).stream()
    cart_data = []
    tot = 0
    length = 0
    for c in cart:
        ca = c.to_dict()
        pdt = db.collection("tbl_vegetable").document(ca["product_id"]).get().to_dict()
        cart_data.append({"cart":ca,"id":c.id,"product":pdt})
        length =length + len(ca)
        tot = tot + int(ca["cart_qty"]) * int(pdt["vegetable_price"])
    # print(cart_data)
    count = int(length/4)
    if request.method == "POST":
        return redirect("webuser:payment")
    else:
        return render(request,"User/MyCart.html",{"cart":cart_data,"count":count,"total":tot})

def deletecartitem(request,cid):
    db.collection("tbl_cart").document(cid).delete()
    return render(request,"User/MyCart.html",{"msg":"Item Deleted form the cart"})

def ajaxmycart(request):
    cart_data = []
    db.collection("tbl_cart").document(request.GET.get("cartid")).update({"cart_qty":request.GET.get("qty")})
    return render(request,"User/AjaxCart.html")


def payment(request):   
    if request.method == "POST":
        bkid = ""
        booking = db.collection("tbl_booking").where("user_id", "==", request.session["uid"]).where("booking_status", "==", 0).stream()
        for i in booking:
            bkid=i.id
        print(bkid)
        cart = db.collection("tbl_cart").where("booking_id", "==", bkid).stream()
        for c in cart:
            ca = c.to_dict()
            pdt = db.collection("tbl_vegetable").document(ca["product_id"]).get().to_dict()
            oldstock = pdt["vegetable_stock"]
            quantity = ca["cart_qty"]
            bal = int(oldstock) - int(quantity)
            db.collection("tbl_vegetable").document(ca["product_id"]).update({"vegetable_stock":bal})
            db.collection("tbl_cart").document(c.id).update({"cart_status":1})
        db.collection("tbl_booking").document(bkid).update({"booking_status":1})
        return redirect("webuser:loader")
        # return render(request,"User/Payment.html")
    else:
        return render(request,"User/Payment.html")

def loader(request):
    return render(request,"User/Loader.html")

def paymentsuc(request):
    return render(request,"User/Payment_suc.html")

def UserComplaints(request):
    id=request.session["uid"]

    compdata=db.collection("tbl_complaints").where("uid", "==", request.session["uid"]).stream()
    complist=[]
    for i in compdata:
        comp=i.to_dict()
        complist.append({"comp_data":comp,"id":i.id})
        
    if request.method=="POST":
        data={"complaint_title":request.POST.get("txtctitle")
            ,"complaint_content":request.POST.get("txtccontent"),"uid":id,"farmer_id":0}
        db.collection("tbl_complaints").add(data)
        return redirect("webuser:UserComplaints")
    else:
        return render(request,"User/UserComplaints.html",{"data":complist})

from django.shortcuts import render, redirect
from firebase_admin import firestore
from datetime import datetime

# Assuming you have initialized Firebase Admin SDK elsewhere in your code.

def userfeedback(request):
    id = request.session["uid"]
    if request.method == "POST":
        data = {
            "feedback_content": request.POST.get("txtfcontent"),
            "uid": id,
            "fid": 0,
            "feedback_time": datetime.now()
        }
        db = firestore.client()  # Initialize Firestore client
        db.collection("tbl_feedbacks").add(data)
        return redirect("webuser:userfeedback")
    else:
        return render(request, "User/UserFeedback.html")



def mybooking(request):
    user_id = request.session.get("uid")
    complist = []
    compdata = db.collection("tbl_booking").where("user_id", "==", user_id).where("booking_status", ">=", 1).stream()
    
    for booking in compdata:
        comp = booking.to_dict()
        cdata = db.collection("tbl_cart").where("booking_id", "==", booking.id).stream()
        for cart_item in cdata:
            cdata_dict = cart_item.to_dict()
            pdata = db.collection("tbl_vegetable").document(cdata_dict["product_id"]).get().to_dict()
            price = pdata["vegetable_price"]
            qty = cdata_dict["cart_qty"]
            total = int(price) * int(qty)
            complist.append({"data": booking.to_dict(), "id": booking.id,"total":total})
    # print(complist)
    return render(request, "User/MyBooking.html",{"complist":complist})
    
def myproduct(request,id):
    complist = []
    cdata = db.collection("tbl_cart").where("booking_id", "==", id).stream()
    for cart_item in cdata:
        cdata_dict = cart_item.to_dict()
        pdata = db.collection("tbl_vegetable").document(cdata_dict["product_id"]).get().to_dict()
        complist.append({"data": cart_item.to_dict(),"product":pdata, "id": cart_item.id})
    # print(complist)
    return render(request, "User/My_Product.html",{"complist":complist})    

def bills(request,id):
    bill = []
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    cdata = db.collection("tbl_cart").where("booking_id", "==", id).stream()
    bk = db.collection("tbl_booking").document(id).get().to_dict()
    invoice = random.randint(111111,999999)
    total = ""
    for cart_item in cdata:
        cdata_dict = cart_item.to_dict()
        pdata = db.collection("tbl_vegetable").document(cdata_dict["product_id"]).get().to_dict()
        price = pdata["vegetable_price"]
        qty = cdata_dict["cart_qty"]
        total = int(price) * int(qty)
        bill.append({"data":cdata_dict,"product":pdata})
    return render(request,"User/Bills.html",{"user":user,"total":total,"booking":bk,"ran":invoice,"bill":bill})

def rating(request,id):
    if 'uid' in request.session:
        parray=["1","2","3","4","5"]    
        bdata = db.collection("tbl_cart").document(id).get().to_dict()
        pdata=db.collection("tbl_vegetable").document(bdata["product_id"]).get().to_dict()
        codata=db.collection("tbl_farmer").document(pdata["farmer_id"]).get().to_dict()
        
        count = 0
        r_len = 0
        r_data = []
        rate = db.collection("tbl_rating").where("farmer_id", "==", pdata["farmer_id"]).stream()
        for i in rate:
            rdata = i.to_dict()
            r_len = r_len + int(len(rdata))
        rlen = r_len // 5
        if rlen>0:
            res=0    
            ratedata = db.collection("tbl_rating").where("farmer_id", "==", pdata["farmer_id"]).stream()
            for i in ratedata:
                rated = i.to_dict()
                r_data.append({"data":i.to_dict()})
                res = res + int(rated["rating_data"])
                avg = res//rlen
            return render(request,"User/Rating.html",{"id":id,"data":r_data,"ar":parray,"avg":avg,"count":rlen})
        else:
            return render(request,"User/Rating.html",{'id':id})
    else:
        return redirect("webguest:login")

def ajaxrating(request):
    parray=[1,2,3,4,5]
    rate_data = []
    bdata = db.collection("tbl_cart").document(request.GET.get('workid')).get().to_dict()
    pdata=db.collection("tbl_vegetable").document(bdata["vegetable_id"]).get().to_dict()
    codata=db.collection("tbl_farmer").document(pdata["farmer_id"]).get().to_dict()
    
    datedata = date.today()
    db.collection("tbl_rating").add({"rating_data":request.GET.get('rating_data'),"user_name":request.GET.get('user_name'),"user_review":request.GET.get('user_review'),"farmer_id":pdata["farmer_id"],"date":str(datedata)})
    pdt = db.collection("tbl_rating").where("farmer_id", "==", pdata["farmer_id"]).stream()
    for p in pdt:
        rate_data.append({"rate":p.to_dict(),"id":p.id})
    return render(request,"User/AjaxRating.html",{'data':rate_data,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    bdata = db.collection("tbl_cart").document(request.GET.get("pdt")).get().to_dict()
    pdata=db.collection("tbl_vegetable").document(bdata["product_id"]).get().to_dict()
    codata=db.collection("tbl_farmer").document(pdata["farmer_id"]).get().to_dict()
    
    rate = db.collection("tbl_rating").where("farmer_id", "==", codata["farmer_id"]).stream()
    for i in rate:
        rated = i.to_dict()
        if int(rated["rating_data"]) == 5:
            five = five + 1
        elif int(rated["rating_data"]) == 4:
            four = four + 1
        elif int(rated["rating_data"]) == 3:
            three = three + 1
        elif int(rated["rating_data"]) == 2:
            two = two + 1
        elif int(rated["rating_data"]) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        r_len = r_len + int(len(rated))
    rlen = r_len // 5
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":rlen}
    return JsonResponse(result)

