from cmath import log
from tkinter import E
from django.shortcuts import redirect, render , get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate , login , logout 
from django.http import HttpResponseRedirect,HttpResponse
from accounts.models import *
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from products.models import *
from ecom.settings import *
from django.urls import reverse
from products.models import *
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count, F
from .forms import WebsiteRatingForm
from .models import WebsiteRating




from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.contrib.auth.decorators import login_required

from django.conf import settings


def search(request):

    query = request.GET.get('search', '')


    is_voice_query = request.GET.get('voice_query', 'false').lower() == 'true'

    if is_voice_query:
        # Process the voice query
        # You can add custom logic here to handle voice search differently
        response_data = {'result': f'Searching for products related to "{query}" (voice query).'}
        return JsonResponse(response_data)


    # Products = Product.objects.all()
    Products = Product.objects.filter(product_name__icontains = query)
    params = {'products': Products}
    return render(request, 'accounts/search.html', params)
    # return HttpResponse("this is search  ")



from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product

def compare_products(request):
    products = Product.objects.all()

    if request.method == 'GET':
        product_slug1 = request.GET.get('product_slug1')
        product_slug2 = request.GET.get('product_slug2')

        if product_slug1 and product_slug2:
            product1 = get_object_or_404(Product, slug=product_slug1)
            product2 = get_object_or_404(Product, slug=product_slug2)

            # Now you have product1 and product2 for comparison
            # You can pass these to the context and display their details in the template

            context = {'product1': product1, 'product2': product2}
            return render(request, 'accounts/compare.html', context)

    context = {'products': products}
    return render(request, 'accounts/compare.html', context)


from random import shuffle
def index(request):
    products = Product.objects.all()
    shuffled_products = list(products)
    shuffle(shuffled_products)  # Shuffle the list of products

    return render(request, 'accounts/order_history.html', {'products': shuffled_products})



# def rate_product(request, product_name):
#     if request.method == 'POST':
#         product = Product.objects.get(id=product_name)
#         rating = int(request.POST.get('rating', 0))

#         # Update the product's average rating
#         product_ratings = product.customerreview_set.all()
#         total_ratings = len(product_ratings)
#         total_sum_ratings = sum(review.rating for review in product_ratings)
#         product.average_rating = total_sum_ratings / total_ratings if total_ratings > 0 else None
#         product.save()

#     # Redirect back to the cart page
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def rate_website(request):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))
        
        # Assuming you have a user associated with the request
        user = request.user

        # Save the rating to the WebsiteRating model
        WebsiteRating.objects.create(user=user, rating=rating_value)

        # You can return a JsonResponse if needed
        return JsonResponse({'message': 'Rating submitted successfully'})

    # Redirect to a specific page if it's not a POST request
    return redirect('home')  # Replace 'home' with the desired URL

def view_ratings(request):
    try:
        # Retrieve all website ratings
        ratings = WebsiteRating.objects.all()
    except Exception as e:
        # Handle any exceptions or errors here
        error = str(e)
        return render(request, 'accounts/view_ratings.html', {'error': error})

    return render(request, 'accounts/view_ratings.html', {'ratings': ratings})


# def rate_website(request):
#     if request.method == 'POST':
#         rating = request.POST.get('rating')

#         if not rating or not rating.isdigit():
#             return JsonResponse({'error': 'Invalid rating value'})

#         rating_value = int(rating)

#         # Check if the user has already rated the website (you can customize this logic)
#         existing_rating = WebsiteRating.objects.filter(user=request.user).first()
#         if existing_rating:
#             existing_rating.rating = rating_value
#             existing_rating.save()
#         else:
#             WebsiteRating.objects.create(user=request.user, rating=rating_value)

#         return JsonResponse({'message': 'Rating saved successfully'})

#     return JsonResponse({'error': 'Invalid request method'})



def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')

def logout(request, *args, **kwargs):
    try:
        print(request.user)
        auth.logout(request)
        print("loged out: ", request.user)
    except Exception as e:
        print(e)
    return redirect('login')



def about_us(request):
    # Your view logic here
    return render(request ,'accounts/about_us.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_line = request.POST.get('first_line')
        second_line = request.POST.get('second_line')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        state = request.POST.get('state')


        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = user_obj
            address.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')




 

def activate_email(request, email_token):
    try:
        # The rest of your code remains the same
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Profile.DoesNotExist:
        print("Profile with email_token does not exist.")
        return HttpResponse('Invalid Email token')
    except Exception as e:
        print("Error:", e)
        return HttpResponse('An error occurred during activation.')
  # Return an error message


def add_to_cart(request, uid):
    try:
        variant = request.GET.get('variant') 

        product = Product.objects.get(uid=uid)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
        cart_item = CartItems.objects.create(cart=cart, product=product)
        
        if variant:
            variant = request.GET.get('variant')
            size_variant = SizeVariant.objects.get(size_name=variant)
            cart_item.size_variant = size_variant
            cart_item.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        # Handle other exceptions or errors here
        print(e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





def remove_cart(request , cart_item_uid):
    try:
         cart_item = CartItems.objects.get(uid= cart_item_uid)
         cart_item.delete()
    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def cart(request):
    user_cart = None
    try:
        user_cart = Cart.objects.get(is_paid=False, user=request.user)
    except Cart.DoesNotExist:
        pass # If no cart matching the conditions is found, create an empty cart.
          # No need to print anything here; just pass

    cart_total = user_cart.get_cart_total() if user_cart else 0  # Calculate the total or set it to 0 if cart is None

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon brooo')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user_cart and user_cart.coupon:
            messages.warning(request, 'Coupon already exists brooooo')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user_cart and user_cart.get_cart_total() > coupon_obj[0].minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user_cart and coupon_obj[0].is_expired:
            messages.warning(request, 'Coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user_cart:
            user_cart.coupon = coupon_obj[0]
            user_cart.save()

            messages.success(request, 'Coupon used')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if user_cart:
        client = razorpay.Client(auth=(settings.KEY, settings.SECERET))
        payment = client.order.create({'amount': user_cart.get_cart_total() * 100, 'currency': 'INR', 'payment_capture': 1})

        user_cart.razor_pay_order_id = payment['id']
        user_cart.save()

    context = {'user_cart': user_cart, 'payment': payment if user_cart else None}
    return render(request, 'accounts/cart.html', context)

def remove_coupon(request, cart_id):
    cart =  Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon Removed ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def success(request):
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(razor_pay_order_id=order_id)
    cart.is_paid = True
    cart.save()

    # Retrieve the user's address
    user_address = None
    try:
        user_address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        pass  # Handle the case where the user's address doesn't exist

    response_text = "Payment Successful"

    if user_address:
        response_text += f"<br><br>Your items will be delivered to the following address:<br><br>"
        response_text += f"{user_address.first_line}<br>"
        response_text += f"{user_address.second_line}<br>"
        response_text += f"{user_address.city}, {user_address.state} {user_address.zip_code}<br>"

    # Add a link to download the bill
    response_text += f'<br><a href="{reverse("generate_bill", args=[order_id, cart.razor_pay_payment_id])}">Download Bill</a>'

    return HttpResponse(response_text)



@login_required
def order_history(request):
    try:
        #  all paid carts associated with the user``
        user_carts = CartItems.objects.filter(cart__user=request.user, cart__is_paid=True)
        user_purchases = Purchase.objects.filter(user=request.user)
        purchased_product = user_purchases.values_list('product', flat=True)

        recommended_products = Product.objects.exclude(
             Q(category__products__purchase__user=request.user) &
             Q(category__products__purchase__product__in=purchased_product)
         ).distinct()


        # Shuffling recommended products
        shuffled_products = list(recommended_products)
        shuffle(shuffled_products)


        
        context = {
            'ordered_items': user_carts,
            'user_cart': user_carts.first().cart if user_carts.exists() else None,  # Get the first cart in case of multiple orders
            'recommended_items': user_purchases,  
            'recommended_products': recommended_products,
            
        }
        return render(request, 'accounts/order_history.html', context)
    except CartItems.DoesNotExist:
        # Handle the case where the user's cart items don't exist or are not paid
        return render(request, 'accounts/order_history.html', {})


# def order_history(request):
#     try:
#         user_carts = CartItems.objects.filter(cart__user=request.user, cart__is_paid=True)
#         user_purchases = Purchase.objects.filter(user=request.user)
#         purchased_product = user_purchases.values_list('product', flat=True)

#         # Find recommended products based on other users who purchased similar products
#         recommended_products = Product.objects.annotate(
#             purchase_count=Count('category__products__purchase'),
#             user_purchase_count=Count('category__products__purchase__user', distinct=True),
#             similarity=F('user_purchase_count') / (F('purchase_count') + 1)  # Add 1 to avoid division by zero
#         ).order_by('-similarity').exclude(id__in=purchased_product)[:5]

#         context = {
#             'ordered_items': user_carts,
#             'user_cart': user_carts.first().cart if user_carts.exists() else None,
#             'recommended_items': user_purchases,
#             'recommended_products': recommended_products,
#         }

#         return render(request, 'accounts/order_history.html', context)
#     except CartItems.DoesNotExist:
#         return render(request, 'accounts/order_history.html', {})

@login_required
def user_details(request):
    user = request.user
    return render(request, 'accounts/user_details.html', {'user': user})

def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user if request.user.is_authenticated else None
            message.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('contact_us')
    else:
        form = ContactMessageForm()
    
    return render(request, 'accounts/contact_us.html', {'form': form})


def generate_bill(request, order_id, payment_id):
    # Get user's address
    try:
        user_address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        user_address = None

    #  authenticated user's name
    user_name = request.user.get_full_name()

    #  response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{order_id}.pdf"'

    #  PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # styles for the PDF content
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    heading_style = styles['Heading1']

    #  title  PDF
    elements.append(Paragraph("Order Bill", heading_style))
    elements.append(Spacer(1, 12))

    #  thank you message
    thank_you_text = f"Thank you, {user_name}, for your order!"
    elements.append(Paragraph(thank_you_text, normal_style))
    elements.append(Spacer(1, 12))

    #  user's address
    if user_address:
        address_text = f"Your items will be delivered to the following address:\n{user_address.first_line}, {user_address.second_line}, {user_address.city}, {user_address.state}, {user_address.zip_code}"
        elements.append(Paragraph(address_text, normal_style))
        elements.append(Spacer(1, 12))

    #  a list of ordered items for the table
    ordered_items = CartItems.objects.filter(cart__razor_pay_order_id=order_id)
    item_data = [["Item", "Price"]]
    for cart_item in ordered_items:
        item_data.append([cart_item.product.product_name, f"RS: {cart_item.product.price}"])

    # table and  its style
    item_table = Table(item_data, colWidths=[300, 100])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    #  table to the PDF elements
    elements.append(Paragraph("Ordered Items:", heading_style))
    elements.append(Spacer(1, 12))
    elements.append(item_table)

    # order ID 
    order_payment_text = f"Order ID: {order_id}"
    elements.append(Paragraph(order_payment_text, normal_style))

    # Add delivery information
    delivery_info = "Your items will be delivered in 1-2 weeks."
    elements.append(Paragraph(delivery_info, normal_style))

    #  PDF document
    doc.build(elements)

    return response
