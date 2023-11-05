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
                    "profile_pic":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJIAAACSCAMAAACZpWO8AAAAY1BMVEX///8AAAD6+vqgoKA1NTULCwvr6+uurq5LS0slJSXm5uYEBATb29vCwsKpqamcnJzOzs51dXVXV1dFRUXx8fHIyMgYGBi1tbVcXFxra2uJiYkcHBwtLS0RERF8fHw+Pj6UlJSaaxB/AAAELUlEQVR4nO2a25aqMAyGC0WEWhUQRdCRef+n3A0gSA8K2uKsvfLdDVPsT5Mm6YEQBEEQBEEQBEEQBEEQBEGQ/wOfb3d0v6e7Lfe/rYWQ8Egzb0RGj+H39PhJefA0HMrkO6PF6WpQsYqDIH78m/LFBYXV1fM2ovNTkK4TzlgYMsaTdRqcvOYf12pZ+/m0G4x0zeT/seLWDRdd0HxJ1AxERHN9pzntGiRLKdq3/RXP2hStqP0igvJm1gfrF1bx10ETE3L3ilgz71PFhTQt0yYiTGj5GRy6uSg2y8V8C5UBKS7Q2nE44DEokjs5Vuc6jutzdZSbX4RDxU41MfjqszQaRTyEyLgYu1h+hqcObZcfxEfXY0V+Os4mqaSpFq8c3Pl4po4Ru8oZ7joek2acMleK9uBH0hgFatYNpHECH3cUnxKNZ6eqImG7cRsOmpzEcV/EY0+a/VudIs/bjlsV4lHkIt9R4afS95NYLymWmqXiVWpfUQ5eIs3mRK9IMRMTHrexX6tU4kvXyjMDldRwLV6Wn30MhG3ZH/yzSdJZbin80HoQp6pvk1BbeQMH2Urg4Za9yReFYiQ/ZJqg1CI7HSFimH7sTrpEOMPuE0k78QN2Y1MppoySqGYYjuSixCxtKoLOb8pTvzRJKlUb3XRCP+AoupEjAJkRBAjEAc+Ty6lPEPPtpCl6poZKgJ3szjlRlQS657VeUa1rG9itUTwlvbdMS7stUDTYU+TrXYk0TquiTgQAnMleZOJ69wCxmjhw0HcMjmcvp2zNvxZGsqLIMNW5yaJvsfO8lWmV4Uu2u5mMw0ROUhLA24gYEJvD3PFhoCJz6GGxzSgg1gHBs8jLf8usrrPy95mvhIHNVcErSQRW4Or626UkMJzel/ykGq9v/aI66r3JruGM7l1AXRnt+xFke/Crs3bnya57G4LAtg9Kl/SX0qq89KFJM9vtBgFtqMy1kbuPBYpn2Q2VuoTCjSVlSyB3bzehaNKuIeE+IlnJbtpVi5PipaCNrMlycSKXcBPGSB4n2yWcVOjyn2mSVg/+ZLvQHS8H8rg5qphgu3iYd7aXA7BoWvU/b1wFqPTrgnxledEkLDcsLV+79gP3QA5LS5t2E5HpZ1iAK7uTz7h2L9lfgD9sU+zmKLrPCgfbFMNmjp+9VDEia15ysZnTb3lNDEkD4EFOtrz6jUHtHu4z0m6LxcEhJm1/fq4iSGzwGQ62T7tNZj5fEne2ydwUPMFsu4mhBbM5OlKFA4tpqUTB2YHqzPk/4OxYBw6/3qJ2eMDL3pPk9HiXG05NnuH2ILU7bp6H89snbKY/uT+Uv19dmMoSVxdIF5+mscwFD9Jeg5nCctdg4LLQhCC+WfKyEOmuVD0jXvhKFTC6eCbzjYtnwJ+7ntfw1y4x3vlbVz0RBEEQBEEQBEEQBEEQBEGs8A8CbCoRiM0vOwAAAABJRU5ErkJggg=="
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