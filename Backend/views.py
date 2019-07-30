from django.shortcuts import render,reverse,redirect,HttpResponse,get_object_or_404
from View.models import Deals,Profile,Mydeals,Request
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.contrib import auth
import random
from Backend.sms import SMS
from Backend.mymail import MAIL
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
# Create your views here.
def index(request):
    deal = Deals.objects.all()
    return render(request,'backend/index.html',{'deal':deal})
def manage_user(request):
    profile=Profile.objects.all()
    users = User.objects.all()
    return render(request,'backend/manage-user.html',{'users':users,'profile':profile})
#Manage Use Details
def user_detail(request,pk):
    user = get_object_or_404(User,pk=pk)
    profile = get_object_or_404(Profile,user_id=user.pk)
    return render(request,'backend/user-detail.html',{'user':user,'profile':profile})
#User administration
@csrf_exempt
@require_http_methods(['POST'])
def user_manage(request):
    payload= request.POST.get('payload',None)
    token= request.POST.get('token',None)
    user = get_object_or_404(User,pk=token)


    
    if payload == "staff":
        content_type = ContentType.objects.get_for_model(Profile)
        permission = Permission.objects.get(codename='is_staff',content_type=content_type,)
        user.user_permissions.add(permission)

        user.save()      

        data ={'msg':'Approved'}      
        return JsonResponse(data)
    elif payload == "suspend":
        user.is_active = False
        user.save()
        data={'msg':'suspended'}
        return JsonResponse(data)
    elif payload == "enable":
        user.is_active = True
        user.save()
        data={'msg':'enabled'}
        return JsonResponse(data)
    else:
        user.delete()
        data={'msg':'deleted'}
        return JsonResponse(data)
    return redirect('Backend:index')
#Deal Request
def save_deal(request,token):
    track_code =   random.randint(100,1000)
    deal = get_object_or_404(Deals,token=token)
    if request.user.is_authenticated:
        uid = request.session['userId']
        user = get_object_or_404(User,pk=uid)
        mydeal = Mydeals.objects.create(deal_code=track_code)
        mydeal.save()
        mydeal.title=deal.title
        mydeal.deal_id=deal
        mydeal.owner = user
        mydeal.save()
        return redirect('View:mydeal')
    else:
        request.session['deal']=token
        return redirect('View:sign-up')
    return HttpResponse('Error')

#Deal Validation
def deal_details(request,pk):
    deal =get_object_or_404(Deals,pk=pk)
    uid=deal.op_id
    profile = get_object_or_404(Profile,pk=uid)
    
    user = get_object_or_404(User,pk=profile.user_id)
    return render(request,'backend/manage-deal.html',{'deal':deal,'profile':profile,'user':user})
#Deal Status
@csrf_exempt
@require_http_methods(['POST'])
def deal_status(request):
    payload= request.POST.get('payload',None)
    token= request.POST.get('token',None)
    uid = request.session['userId']
    user = get_object_or_404(User,pk=uid)


    deal= get_object_or_404(Deals,token=token) 
    deal.moderator=user
    deal.save()
    if payload == "approve":
        deal.valid=True
        deal.is_valid=True

        deal.save()      
        userename=user.first_name
        email=user.email
        data ={'msg':'Approved'}
        deal.status =True
        deal.save()
             
        return JsonResponse(data)
    elif payload == "decline":
        deal.valid =False
        deal.save()
        data={'msg':'Declined'}
        deal.status = False
        deal.save()
         
        return JsonResponse(data)

    elif payload == "suspend":
        deal.status = False
        deal.save()
        data={'msg':'Suspended'}
         
        return JsonResponse(data)
    else:
        deal.delete()
        data ={'msg':'deleted'}
        return JsonResponse(data)
    return redirect('Backend:index')

@csrf_protect
@require_http_methods(['POST'])
def save_deals(request):
    title= request.POST.get('title',None)
    about = request.POST.get('about',None)
    uid = request.session['userId']
    user = get_object_or_404(User,pk=uid)
    req = Request.objects.create(title=title,text=about,op=user)
    req.save()
    return redirect('View:dashboard')

#DEAL REQUEST RECORD
def deal_record(request):
    mydeal= Mydeals.objects.all()
    return render(request,'backend/deal_record.html',{'mydeal':mydeal})
#DEAL REQUEST MODERATION
def deal_moderation(request,code):
    mydeal= get_object_or_404(Mydeals, deal_code=code)
    #Get the Deal object
    deal_id = mydeal.deal_id_id
    deal = get_object_or_404(Deals,pk=deal_id)
    # Deal owner object
    deal_owner = deal.op_id
    profile_owner = get_object_or_404(Profile,pk=deal_owner)
    owner = get_object_or_404(User,pk=profile_owner.user_id)
    #Deal Request owner objeck
    request_user =get_object_or_404(User,pk=mydeal.owner_id)
    #Request Owner Profile
    profile_request =get_object_or_404(Profile,user_id=request_user.id)
    return render(request,'backend/request-details.html',{'mydeal':mydeal,'deal':deal,'owner':owner,'profile':profile_request,
                                                        'req':request_user,'profile_owner':profile_owner})
@csrf_exempt
@require_http_methods(['POST'])
def approve_request(request):
    payload= request.POST.get('payload',None)
    token= request.POST.get('token',None)


    deal= get_object_or_404(Mydeals,deal_code=token) 
    deal.save()
    if payload == "approve":
        deal.is_fufilled=True
        deal.save()
        deal.save()  
        deal.status='successful'    
        data ={'msg':'Approved'}
        deal.save()    
          
        return JsonResponse(data)
    elif payload == "decline":
        deal.is_fufilled =False
        deal.save()
        deal.status='declined'
        deal.save()
        data={'msg':'Declined'}
        deal.save()
         
        return JsonResponse(data)
    return redirect('Backend:request-record')

def users_record(request):
    users= User.objects.all()
    return render(request,'backend/manage-user.html',{'user':users})

#Settings
def settings(request):
    return render(request,'backend/settings.html')