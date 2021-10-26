from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView    
from django.http import HttpResponse
from .models import Payments
from django.utils import timezone
from rest_framework import generics
import time

from django.contrib import messages

from .serializers import PaymentsSerializer

import json
import requests 

ocp= "f60159945e2142008839ae38714d7518"  # move to environ variables in production
apikey="bcb7cfbc162c4e8dbe0098c05a144a52"  # move to environ variables in production
authorization="Basic YmM5M2Q4NzYtNzdjYS00N2RmLWI4NjItYmYyYTFmNTZlY2VlOmJjYjdjZmJjMTYyYzRlOGRiZTAwOThjMDVhMTQ0YTUy" #move to environ variables in production


def authoo():
    reqUrl = "https://sandbox.momodeveloper.mtn.com/disbursement/token/"
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.io)",
    "Ocp-Apim-Subscription-Key": ocp,
    "Authorization": authorization 
    }
    #authorization is generated from    ocp sub key and Apikey
    payload = ""
    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
    res=json.loads(response.text)
    #print(res)
    #print(res.get('access_token'))
    if res.get('access_token'):
        return 'Bearer '+res.get('access_token')


# api view when using django rest framework
class Paymentslist(generics.ListAPIView):   
    queryset = Payments.objects.filter(status="SUCCESSFUL") #api view for successfull transactions
    serializer_class = PaymentsSerializer


class userLogin(LoginView):
    template_name = 'login.html'


def index(request):
    context = {}
    return render(request, 'index.html' , context)


@login_required
def payment(request):
    global autho
    
    autho=authoo()
    if not autho:
        messages.success(request,'Error Authenticating momo API')

    if request.method == "POST":
        data= request.POST
        names=[]
        nums=[]
        amts=[]
        bkts=[]
        comm=[]
        ptype=[]
        
        for i,v in data.items():
            if i.startswith('name'):
                names.append(v) 
            elif i.startswith('number'):
                nums.append(v)
            elif i.startswith('amt'):
                amts.append(v)
            elif i.startswith('bkt'):
                bkts.append(v)
            elif i.startswith('comm'):
                comm.append(v)
            elif i.startswith('ptype'):
                ptype.append(v)

        data_list= list(zip(names,nums,amts,bkts,comm,ptype))
        
        import uuid
        for i in data_list:            
            if i[0] and i[1] and i[2] and i[3]:                
                uid=uuid.uuid4() #generate unique uuid per request row                
                postreqUrl = "https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/transfer" #for posting transfer request info
                getreqUrl = f"https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/transfer/{uid}" #for getting status of each transfer
                
                #for posting each transfer request info
                headersList1 = {
                "Accept": "*/*",
                "User-Agent": "Thunder Client (https://www.thunderclient.io)",
                "X-Reference-Id": str(uid),
                "X-Target-Environment": "sandbox",
                "Ocp-Apim-Subscription-Key": ocp,
                "Authorization": autho,
                "Content-Type": "application/json" 
                }
                
                #for getting each transfer response info
                headersList2 = {
                "Accept": "*/*",
                "User-Agent": "Thunder Client (https://www.thunderclient.io)",               
                "X-Target-Environment": "sandbox",
                "Ocp-Apim-Subscription-Key": ocp,
                "Authorization": autho
                }

                #converting number to int format 
                intnum=str(i[1])
                if intnum.startswith('0'):
                    mnumber='233'+intnum[1:]
                else:
                    mnumber=str(i[1])
                
                payload = {"amount": str(i[2]), "currency": "EUR","externalId": "12345","payee": {"partyIdType": "MSISDN", "partyId": mnumber }, "payerMessage": str(i[3]) ,  "payeeNote": "By accepting this payment, be aware that your payment details will be shared with third parties."} #for posting transfer request info
                response1 = requests.request("POST", postreqUrl, data=json.dumps(payload),  headers=headersList1) # response from transfer stage
                ii=response1  
                
                
                
                if ii:
                    response2 = requests.request("GET", getreqUrl, data="",  headers=headersList2)
                    #print('bbbbb',response2.json())
                    iii=json.loads(response2.text)  
                    
                    time.sleep(5)             
                    pay=Payments.objects.create(date=timezone.now(),transactionId=iii.get('financialTransactionId'),extid=iii.get('externalId'),amountPaid=iii.get('amount'),name=i[0],productType=i[5],community=i[4],phoneNumber=iii.get('payee',{}).get('partyId'),reason=iii.get('reason'),numberOfBuckets=i[3],status=iii.get('status'),paid_by=request.user.username)
                    pay.save() 
                #end

        return redirect('history')

    headersList3 = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.io)",               
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": ocp,
            "Authorization": autho           
            }

    balreqUrl = "https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/account/balance" #for getting account balance

    response4 = requests.request("GET", balreqUrl, data="",  headers=headersList3) #getaccountbalance
    
    yy='Unavailable'
    if response4:
        vvy=json.loads(response4.text)
        yy=vvy.get('availableBalance') 

    if request.user.groups.all()[0].name=='fieldofficers': 
        context = {}
    else:
        context={'bal':f'Account Balance: {yy}'}
    return render(request, 'payment.html' , context)
    

@login_required
def history(request):
    if request.user.groups.all()[0].name=='fieldofficers': 
        payments=Payments.objects.filter(paid_by=request.user).order_by('-date')
    else:
        payments=Payments.objects.all().order_by('-date')
  
    context = {'payments':payments} 
    return render(request, 'payment_history.html' , context)


