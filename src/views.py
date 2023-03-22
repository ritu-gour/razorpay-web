from django.shortcuts import render
from .forms import CoffeePaymentForm
import razorpay
from .models import Coldcoffee
# Create your views here.

def coffee_payment(request):
    if request.method == 'POST':
     name =  request.POST.get('name')  
     amount = int(request.POST.get('amount')) * 100
    
     client = razorpay.Client(auth=('rzp_test_JVzDj0di6ZNHsZ','TAchASYuiY2v73rr3JxsQx0I'))
     
     response_payment = client.order.create(dict(amount=amount,
                                                 currency='INR')
                                                 )
    #  print(response_payment)
     order_id = response_payment['id']
     order_status = response_payment['status']
     if order_status== 'created':
      cold_coffee = Coldcoffee(
          name = name,
          amount = amount,
          order_id = order_id
      )
      cold_coffee.save()
      response_payment['name'] = name


      return render(request,'coffee_payment.html', {'payment': response_payment})
      
    return render(request,'coffee_payment.html',)


def payment_status(request):
  response = request.POST
#   print(response)
  params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature_id': response['razorpay_signature_id']
  }

  client = razorpay.Client(auth=('rzp_test_JVzDj0di6ZNHsZ','TAchASYuiY2v73rr3JxsQx0I'))
  try:
    status = client.utility.verify_payment_signature(params_dict)
    cold_coffee = Coldcoffee.objects.get(order_id = response['razorpay_order_id'])
    cold_coffee.rezorpay_payment_id = response['razorpay_payment_id']
    cold_coffee.paid = True
    cold_coffee.save()
    return render(request,'payment_status.html',{'status':True})
  except :
    return render(request,'payment_status.html',{'status':False})
  

def paymentss(request):
    return render(request,'paymentss.html')