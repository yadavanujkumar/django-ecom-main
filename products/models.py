from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User




class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , null=True , blank=True)
    category_image = models.ImageField(upload_to="catgories")


    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category ,self).save(*args , **kwargs)


    def __str__(self) -> str:
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.size_name




# class Product(BaseModel):
#     product_name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True  , null=True , blank=True)
#     category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name="products")
#     price = models.IntegerField()
#     product_desription = models.TextField()
#     color_variant = models.ManyToManyField(ColorVariant , blank=True)
#     size_variant = models.ManyToManyField(SizeVariant , blank=True)
#     # average_rating = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return f"Model Name for {self.product.product_model_name}"
    
#     def save(self , *args , **kwargs):
#         self.slug = slugify(self.product_name)
#         super(Product ,self).save(*args , **kwargs)


#     def __str__(self) -> str:
#         return self.product_name

#     def get_product_price_by_size(self, size):
#         return self.price + SizeVariant.objects.get(size_name=size).price


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    product_description = models.TextField()  # Corrected the field name
    color_variant = models.ManyToManyField('ColorVariant', blank=True)
    size_variant = models.ManyToManyField('SizeVariant', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_product_price_by_size(self, size):
        size_variant = self.size_variant.filter(size_name=size).first()
        if size_variant:
            return self.price + size_variant.price
        return self.price


class ProductImage(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_images")
    image =  models.ImageField(upload_to="product")

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=1500)

class Purchase(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)