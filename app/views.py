from distutils.log import error
import random
import string
from django.conf import settings
import stripe
import json
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from functools import reduce
from operator import and_

from .forms import CheckOutForm
from .models import Address, Category, Item, Order, OrderItem


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class Home(ListView):
    model=Item
    paginate_by=2
    template_name='home-page.html'

class Detail(DetailView):
    model=Item
    template_name='product-page.html'


@login_required
def add_to_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    qs=Order.objects.filter(user=request.user,ordered=False)
    if qs.exists():
        order=qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
        else:
            order.items.add(order_item)
            messages.info(request,item.title+'をカートに入れました。')

    else:
        order=Order.objects.create(user=request.user)
        order.items.add(order_item)
    return redirect('app:summary')    

@login_required
def remove_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    qs=Order.objects.filter(user=request.user,ordered=False)
    if qs.exists():
        order=qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect('app:summary')
        else:
            return redirect('app:detail', slug=slug)
    return redirect('app:detail', slug=slug)
    
@login_required
def remove_single_item_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    qs=Order.objects.filter(user=request.user,ordered=False)
    if qs.exists():
        order=qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            if order_item.quantity>1:
                order_item.quantity-=1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect('app:summary')
    return redirect('app:detail', slug=slug)


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            context={
                'order':order,
            }
            return render(self.request,'order-summary.html',context)


        except ObjectDoesNotExist:
            return redirect('/')

class CheckOutView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            form=CheckOutForm()
            address=Address.objects.filter(user=self.request.user)
            if address.exists():
                address=address[0]
                if address.default==True:
                    print(address.prefecture)
                    initial_dict={
                    'prefecture': address.prefecture,
                    'street_address': address.street_address,
                    'apartment_address': address.apartment_address,
                    'zip': address.zip,
                    }
                    form=CheckOutForm(self.request.POST or None, initial=initial_dict)
                    
            order=Order.objects.get(user=self.request.user,ordered=False)
            
            context={
                'form':form,
                'order':order,
            }
            return render(self.request,'checkout-page.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request,'エラー発生')
            return redirect('/')
        
        
    
    def post(self, *args, **kwargs):
        form=CheckOutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            address=Address.objects.filter(user=self.request.user)
            
            if form.is_valid():
                if address.exists():
                    address=address[0]
                    address.zip=form.cleaned_data.get('zip')
                    address.prefecture=form.cleaned_data.get('prefecture')
                    address.street_address=form.cleaned_data.get('street_address')
                    address.apartment_address=form.cleaned_data.get('apartment_address')
                else:
                    zip=form.cleaned_data.get('zip')
                    prefecture=form.cleaned_data.get('prefecture')
                    street_address=form.cleaned_data.get('street_address')
                    apartment_address=form.cleaned_data.get('apartment_address')
                    address=Address(
                        user=self.request.user,
                        zip=zip,
                        prefecture=prefecture,
                        street_address=street_address,
                        apartment_address=apartment_address,
                    )

                default=form.cleaned_data.get('default')
                if default:
                    address.default=True
                address.save()
                order.address=address
                order.save()
                return redirect('app:payment')
            else:
              
                return redirect('app:checkout')
        except ObjectDoesNotExist:
            messages.info(self.request,'カートに商品を入れてください。')
            return redirect('app:summary')


class PaymentView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            if not order.address:
                messages.info(self.request,'checkoutを済ませてください。')
                return redirect('/')
            else:
                context={
                    'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY,
                    'order':order,
                    'domain':settings.DOMAIN,
                }
                return render(self.request,'payment.html',context)
        except ObjectDoesNotExist:
            return redirect('/')
    

   
def CreatePayment(request):

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            req_json = json.loads(request.body)
            much=req_json['items'][0]['id']
            intent = stripe.PaymentIntent.create(
                amount=much,
                currency='JPY',
                automatic_payment_methods={
                'enabled': True,
            },
            )
            
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})

# セキュリティー弱い
@login_required
def OrderFinish(request):
        order=Order.objects.get(user=request.user,ordered=False)
        for order_item in order.items.all():
            order_item.ordered=True
            order_item.save()
        
        order.ordered=True
        order.order_date=timezone.now()
        order.ref_code=create_ref_code()
        order.save()
        return redirect('/')

def webhook(request):
    endpoint_secret = settings.ENDPOINT_SECRET
    event = None
    payload = request.data

    try:
        event = json.loads(payload)
    except:
        print('⚠️  Webhook error while parsing basic request.' + str(error))
        return JsonResponse(success=False)
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return JsonResponse(success=False)

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('Payment for {} succeeded'.format(payment_intent['amount']))

        
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return JsonResponse(success=True)


class CategoryView(View):
    def get(self, *args, **kwargs):
        category=Category.objects.get(category=self.kwargs['category'])
        item=Item.objects.order_by('-id').filter(category=category)
        context={
            'object_list':item,
            'keyword':category,
        }
        return render(self.request, 'home-page.html', context)

class SearchView(View):
    def get(self, *args, **kwargs):
        item=Item.objects.order_by('-id')
        keyword=self.request.GET.get('keyword')
        if keyword:
            exclusion_list=set([' ','　'])
            query_list=''
            for word in keyword:
                if not word in exclusion_list:
                    query_list+=word
            query=reduce(and_, [Q(title__icontains=q) | Q(description__icontains=q) for q in query_list])
            item=item.filter(query)
        context={
            'keyword':keyword,
            'object_list':item,
        }
        return render(self.request, 'home-page.html', context)