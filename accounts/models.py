
from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import *
from django import forms


class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False , cart__user = self.user).count()

class Address(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    first_line = models.CharField(max_length=50, null=True, blank=True, default='')
    second_line = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Address for {self.user.username}"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_line', 'second_line', 'zip_code', 'city', 'state']

class ContactMessage(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_messages')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact Message from {self.user.username}"

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message']

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon , on_delete=models.SET_NULL , null=True , blank=True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100, null=True , blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True , blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True , blank=True)



    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant.price
                price.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                price.append(size_variant_price)
        
        
        if self.coupon:
            if self.coupon.minimum_amount < sum(price):
                return sum(price) - self.coupon.discount_price
        
        return sum(price)


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        price = [self.product.price]

        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)
        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        return sum(price)

@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)

from django.db import models

class CustomerReview(models.Model):
    comment = models.TextField()
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)]) 

class WebsiteRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.rating}"


