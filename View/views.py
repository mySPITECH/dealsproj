from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import ProfileForm
from django.contrib.auth.models import User
from .models import Profile,Deals,Cleanser,Mydeals,Request
from .token import RandomToken
from Backend.sms import SMS
from Backend.mymail import MAIL
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from Backend.models import EmailToken
from django.http import JsonResponse
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random


# Create your views here.
def home(request):
    deals =Deals.objects.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(deals, 5)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request,'view/index.html',{'deals':numbers})
def index(request):
    uid= request.session['userId'] 
    user = get_object_or_404(User,pk=uid)
    profile = get_object_or_404(Profile,user=uid)
    return render(request,'view/index.html',{'profile':profile,'user':user})
#Deals detail
def deal_deail(request,pk):
    deal= get_object_or_404(Deals,pk=pk)
    deal.views +=1
    deal.save()
    return render(request,'view/deal-detail.html',{'deal':deal})
#Sign up form
def sign_up(request):
    return render(request,'view/signup.html')
#User sign up during deal creation
@csrf_protect
@require_http_methods(['POST'])
def registar(request):
    first_name =request.POST.get('first_name',None)
    last_name =request.POST.get('last_name',None)

    pword = request.POST.get('password',None)
    email = request.POST.get('email',None)
    phone = request.POST.get('phone',None)
    username = request.POST.get('username',None)

    gender = request.POST.get('gender',None)
    users = User.objects.create_user(username=username,password=pword,last_name=last_name,
                                    email=email,first_name=first_name)
    users.save()
    #user profile
    myprofile = Profile(mobile_no=phone,gender=gender)
    myprofile.save()
    uid = get_object_or_404(Profile,pk=myprofile.id)
    uid.user =users
    uid.save()
    #get deal & save deal
    deal_token= request.session['deal']

    deal = get_object_or_404(Deals,token=deal_token)
    track_code =   random.randint(100,1000)
    mydeal = Mydeals.objects.create(deal_code=track_code)
    mydeal.save()
    mydeal.title = deal.title
    mydeal.save()
    mydeal.deal_id=deal
    mydeal.save()
    mydeal.owner = users
    mydeal.save()
    #User Login Table ID
    myuser =get_object_or_404(User,username=username)
    token = RandomToken.randomString(12)
    #Token that was sent to Email
    tokenize = EmailToken(token=token,uid=myuser.id)
    tokenize.save()
    link = '{}/{}/{}'.format('','welcome',token)
    to=[myuser.email]
    FROM="Deals Connect NG."
    context={'fullname':first_name,'link':link}
    TEMPLATE='email/deal-registration.html'
    Subject = "Account Verification!"
    mssg=MAIL(to,FROM,context,TEMPLATE,Subject)
    mssg.send_mail()
    message="Thanks for Choosing Deals Connect an Email has been sent to your mailbox"
    return render(request,'view/success.html',{'message':message})
#Create Account
@csrf_protect
@require_http_methods(['POST'])
def create_account(request):
    first_name =request.POST.get('first_name',None)
    last_name =request.POST.get('last_name',None)

    pword = request.POST.get('password',None)
    email = request.POST.get('email',None)
    phone = request.POST.get('phone',None)
    username = request.POST.get('username',None)

    gender = request.POST.get('gender',None)
    users = User.objects.create_user(username=username,password=pword,last_name=last_name,
                                    email=email,first_name=first_name)
    users.save()
    #user profile
    myprofile = Profile(mobile_no=phone,gender=gender)
    myprofile.save()
    uid = get_object_or_404(Profile,pk=myprofile.id)
    uid.user =users
    uid.save()
    #User Login Table ID
    myuser =get_object_or_404(User,username=username)
    token = RandomToken.randomString(12)
    #Token that was sent to Email
    tokenize = EmailToken(token=token,uid=myuser.id)
    tokenize.save()
    link = '{}/{}/{}'.format('dealsconnect.herokuapp.com','welcome',token)
    to=[myuser.email]
    FROM="Deals Connect NG."
    context={'fullname':first_name,'link':link}
    TEMPLATE='email/registration.html'
    Subject = "Account Verification!"
    mssg=MAIL(to,FROM,context,TEMPLATE,Subject)
    mssg.send_mail()
    #The token that was sent to user
    print(pword)
    message="Thanks for Choosing Deals Connect an Email has been sent to your mailbox"
    return render(request,'view/success.html',{'message':message})
#Account Verification Login
def verifyAccount(request,token):
    user1 =get_object_or_404(EmailToken,token=token)
    myid=get_object_or_404(User,pk=user1.uid)
    uname= myid.username
    #user1.delete()
    return render(request,'view/login.html',{'username':uname,})
#User Login view  
@csrf_protect
@require_http_methods(['POST'])
def verification_login(request):
    username= request.POST['username']
    password = request.POST['pass']
    user =authenticate(request,username=username,password=password)

    if user is not None:
        auth.login(request,user)
        myuser = get_object_or_404(User,username=username)
        profile = get_object_or_404(Profile,user=myuser.id)
        profile.is_verified=True
        profile.save()
        #set session after sucessful authentication
        request.session['userId'] = myuser.id
        return redirect('View:index')
   
    else:
        return HttpResponse('Unauthorized User')
    return render(request,'view/login.html')
@csrf_protect
@require_http_methods(['POST'])
def login2(request):
    username = request.POST['username']
    password = request.POST['pass']
    user =authenticate(request,username=username,password=password)
    myuser = get_object_or_404(User,username=username)
    request.session['userId'] = myuser.id
    if user is None:
        message = 'invalid username or password'
        return render(request,'view/error.html',{'message':message})
    if user.is_superuser:
        auth.login(request,user)

        return redirect('Backend:web-master')
    else:
        auth.login(request,user)

        return redirect('View:index')
    return HttpResponse('error')
#User log out
def log_uerout(request):
    logout(request)
    return redirect('View:home')
#Profile Page
def user_profile(request):
    uid= request.session['userId'] 
    profile = get_object_or_404(Profile,user=uid)

    return render(request,'view/profile.html',{'profile':profile})

#save Deal
@csrf_protect
@require_http_methods(['POST'])
def save_deal(request):
    uid = request.session['userId'] 
    token = RandomToken.randomString(30)
    about = request.POST.get('about',None) 
    email=request.POST.get('email',None)
    title=request.POST.get('title',None)
    users=get_object_or_404(Profile,user=uid)
    userz=get_object_or_404(User,pk=uid)

    framework = request.POST.getlist('framework[]')
    deal = Deals.objects.create(about=about,title=title,framework=framework,token=token)
    deal.save()
    dealToken = get_object_or_404(Deals,token=token)
    dealToken.op = users
    dealToken.save()
    link = '{}/{}/{}'.format('6c4307c6.ngrok.io','clear_deal',token)
    to=[email]
    FROM="Deals Connect NG."
    context={'fname':userz.first_name,'lname':userz.last_name,'link':link,}
    TEMPLATE='email/deal.html'
    Subject = "Deal Clearance"
    mssg=MAIL(to,FROM,context,TEMPLATE,Subject)
    mssg.send_mail()
    return HttpResponse('An email has been sent to your Referee mail box')

def deal_clearance(request,token):
    deal=get_object_or_404(Deals,token=token)
    #users= get_object_or_404(User,pk=uid)
    
    #profile=get_object_or_404(Profile,user=uid)
    if deal.is_verified == True:
        message='Invalid verification'
        return render(request,'view/error.html',{'message':message})
    else:
        framework=deal.framework
        return render(request,'view/deal-clearance.html',{'deal':deal,'framework':framework,
                        })
    return redirect('View:index')
@csrf_protect
def save_clearance(request):
    token = request.POST.get('token',None)
    fullname = request.POST.get('names',None)
    image= request.POST.get('image',None)
    city = request.POST.get('city',None)
    state =request.POST.get('state',None)
    address =request.POST.get('address',None)
    phone = request.POST.get('phone',None)
    verified_deal = Cleanser.objects.create(names=fullname,address=address,city=city,
                                        state=state,mobile_no=phone,image=image,token=token)
    verified_deal.save()
    deal=get_object_or_404(Deals,token=token)
    deal.is_verified = True
    deal.save()
    return HttpResponse('Deals verified')
#USER REQUEST
def user_deals(request):
    uid =request.session['userId']  
    mydeal= Mydeals.objects.filter(owner_id=uid)
    return render (request,'view/mydeal.html',{'mydeal':mydeal}) 

#Deal Request
def deal_process(request):
    return render(request,'view/deal_request.html')

#Dashboard
def dashboard(request):
    uid=request.session['userId']
    mydeals = Deals.objects.filter(op_id=uid)
    req = Request.objects.filter(op_id=uid)
    return render(request,'view/dashboard.html',{'deal':mydeals,'req':req})







    
