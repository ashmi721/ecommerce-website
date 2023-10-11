from django.shortcuts import render,redirect
from users.forms import UserRegisterForm
from django.contrib import messages
from users.models import User,Profile
from django.contrib.auth import authenticate
# Create your views here.
def home(request):
    return render(request,template_name="index.html")

def user_login(request):
    # if request.method == "POST":
    #     email = request.POST.get("email")
    #     password = request.POST.get("password")
    #     print("Email: ", email, "Password: ", password)
    #     check_user = User.objects.filter(email=email)
    #     if not check_user.exists():
    #         error = "Account does not exists"
    #         messages.error(request, error)
    #         return redirect("/login")
    #     is_valid_user = authenticate(username=check_user[0].username, password=password)
    #     if is_valid_user:
    #         return redirect("/profile")
    #     else:
    #         error = "Invalid Email or Password"
    #         messages.error(request, error)
    #         return redirect("/login")
    return render(request, "login.html")

def user_register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form_data = UserRegisterForm(request.POST)
        if form_data.is_valid():
            print("Form Data:",form_data.changed_data)
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
                "profile_pic":"N/A"
            }
            profile = Profile.objects.create(**profile_data)
            
            print("----*" *50)
            print(form_data.cleaned_data)
            print("----*" *50)
        return redirect("/login")   
    else:
        error = form_data.errors
        messages.error(request,error) 
        return render("/register")
    return render(request,"register.html",{"form":form})
            
   


def user_profile(request):
    return render(request,"profile.html")