from django.shortcuts import render,redirect
from users.forms import UserRegisterForm
from django.contrib import messages
from .models import User,Profile
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from products.models import Products
from users.helper import save_file
# Create your views here.
def home(request):
    products = Products.objects.all()  
    return render(request,template_name="users/index.html", context={"products":products})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Username: ", username, "Password: ", password)
        check_user = User.objects.filter(username=username)
        if not check_user.exists():
            error = "Account does not exists"
            messages.error(request, error)
            return redirect("/login")
        is_valid_user = authenticate(username=check_user[0].username, password=password)
        if is_valid_user:
            login(request,is_valid_user)
            request.session["name"] = is_valid_user.first_name
            return redirect("/profile")
        else:
            error = "Invalid username or Password"
            messages.error(request, error)
            return redirect("/login")
    return render(request, "users/login.html")

def user_register(request):
    form = UserRegisterForm()
    if request.method == "POST":
            form_data = UserRegisterForm(request.POST)
            
            if form_data.is_valid():   
                print("Form Data:",form_data.cleaned_data)
                password = form_data.cleaned_data["password"]
                conform_password = form_data.cleaned_data["conform_password"]
                if password !=conform_password:
                    error = "Password and Conform Password fields does not match"
                    messages.error(request,error)
                    return redirect("/register")
                
                check_user = User.objects.filter(username=form_data.cleaned_data["username"]).exists()
                check_email = User.objects.filter(email=form_data.cleaned_data["email"]).exists()
                if check_user or check_email:
                    error = "Username or Email already exists"
                    messages.error(request,error)
                    return redirect("/register")
                
                user_account_data={
                    "first_name":form_data.cleaned_data["first_name"],
                    "last_name":form_data.cleaned_data["last_name"],
                    "username":form_data.cleaned_data["username"],
                    "email":form_data.cleaned_data["email"]
                }
                user = User.objects.create(**user_account_data)
                user.set_password(password)
                user.save()

                profile_data={
                    "user":user,
                    "contact":form_data.cleaned_data['contact'],
                    "address":form_data.cleaned_data['address'],
                    "city":form_data.cleaned_data['city'],
                    "profile_pic":"https://static.thenounproject.com/png/642902-200.png"
                }
                profile = Profile.objects.create(**profile_data)
                return redirect("/login")   
            else:
                error = form_data.errors
                messages.error(request,error) 
                return redirect("/register")
    return render(request,"users/register.html",{"form":form})
            
@login_required
def user_profile(request):
    User_id = request.user.pk
    profile = Profile.objects.get(user_id=User_id)
    if request.method == "POST":
        city=request.POST.get("city")
        address=request.POST.get("address")
        contact=request.POST.get("contact")
        profile_pic=request.FILES.get("profile_img")
        profile_pic_url = save_file(request,profile_pic)
        print("City: ",city,"Address: ",address,"contact:",contact, "Profile_pic: ",profile_pic_url)
        if city != profile.city:
            profile.city = city
        if address != profile.address:
            profile.address = address
        if contact != profile.contact:
            profile.contact = contact
        if profile_pic_url is not None:
            if profile_pic_url != profile.profile_pic:
                profile.profile_pic = profile_pic_url
        profile.save()
        return redirect("/profile")
    return render(request,"users/profile.html",context={"profile":profile})

def user_logout(request):
    logout(request)
    return redirect("/login")  