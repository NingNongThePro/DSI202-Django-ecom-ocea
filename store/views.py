from django.shortcuts import render,get_object_or_404,redirect
from store.models import Collection,Product,Cart,CartItem,Order,OrderItem
from store.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.conf import settings 
import stripe
# Create your views here.

def home(request,collection_slug=None):
    products=None
    collection_page=None
    if collection_slug != None:
        collection_page=get_object_or_404(Collection,slug=collection_slug)
        products=Product.objects.all().filter(collection=collection_page,available=True)
    else : 
        products=Product.objects.all().filter(available=True)

    return render(request,'home.html',{'products':products,'collection':collection_page})

def login(request):
    return render(request,'login.html')


def productPage(request,collection_slug,product_slug):
    try:
        product=Product.objects.get(collection__slug=collection_slug,slug=product_slug)
    except Exception as e :
            raise e
    return render(request,'product.html',{'product':product})

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

@login_required(login_url='/accounts/login/')
def addCart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    #ซื้อครั้งแรก
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity<cart_item.product.stock :
            cart_item.quantity+=1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('/')
    
def cartdetail(request):
    total=0
    counter=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=item.quantity
    except Exception as e :
        pass
    stripe.api_key=settings.SECRET_KEY
    stripe_total=int(total*100)
    description="Payment Online"
    data_key=settings.PUBLIC_KEY

    if request.method=="POST":
        try :
            token=request.POST['stripeToken']
            email=request.POST['stripeEmail']
            name=request.POST['stripeBillingName']
            address=request.POST['stripeBillingAddressLine1']
            city=request.POST['stripeBillingAddressCity']
            postcode=request.POST['stripeShippingAddressZip']
            customer=stripe.Customer.create(
                email=email,
                source=token
            )
            charge=stripe.Charge.create(
                amount=stripe_total,
                currency='thb',
                description=description,
                customer=customer.id
            )
            #บันทึกข้อมูลใบสั่งซื้อ
            order=Order.objects.create(
                name=name,
                address=address,
                city=city,
                postcode=postcode,
                total=total,
                email=email,
                token=token
            )
            order.save()

            #บันทึกรายการสั่งซื้อ
            for item in cart_items :
                order_item=OrderItem.objects.create(
                    product=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                    order=order
                )
                order_item.save()
                #ลดจำนวน Stock
                product=Product.objects.get(id=item.product.id)
                product.stock=int(item.product.stock-order_item.quantity)
                product.save()
                item.delete()
            return redirect('thankyou')
            

        except stripe.error.CardError as e:
            return False, e
    

    return render(request,'cartdetail.html',
    dict(cart_items=cart_items,total=total,counter=counter,data_key=data_key,stripe_total=stripe_total,description=description))

def removeCart(request,product_id):
    #ทำงานกับตะกร้าสินค้า A
    cart=Cart.objects.get(cart_id=_cart_id(request))
    #ทำงานกับสินค้าที่จะลบ 1
    product=get_object_or_404(Product,id=product_id)
    cartItem=CartItem.objects.get(product=product,cart=cart)
    #ลบรายการสินค้า 1 ออกจากตะกร้า A โดยลบจาก รายการสินค้าในตะกร้า (CartItem)
    cartItem.delete()
    return redirect('cartdetail')

def signup(request):
    return render(request,"signup.html")

def about(request):
    return render(request,"about.html")

def thankyou(request):
    return render(request,"thankyou.html")