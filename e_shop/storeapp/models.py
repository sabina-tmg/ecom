import datetime
from django.db import models
from django.utils import timezone
import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name



class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name



class Filter_price(models.Model):
    FILTER_PRICE = (
        ('1000 To 10000', '1000 To 10000'),
        ('2000 To 20000', '2000 To 20000'),
        ('3000 To 30000', '3000 To 30000'),
        ('4000 To 40000', '4000 To 40000'),
        ('5000 To 50000', '5000 To 50000'),
    )
    price = models.CharField(choices=FILTER_PRICE, max_length=70)
    def __str__(self) -> str:
        return self.price



class Product(models.Model):
    CONDITION = (
        ('New', 'New'),
        ('Old', 'Old'),
    )

    STOCK = (
        ('IN STOCK', 'IN STOCK'),
        ('OUT OF STOCK', 'OUT OF STOCK'),
    )
    
    STATUS = (
        ('publish', 'publish'),
        ('draft', 'draft'),
    )
    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    #unique_id = models.UUIDField(default=uuid.uuid4,editable=False)
    image = models.ImageField(upload_to='product_images/image')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION, max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_price, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.unique_id and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%y%m%d23') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

    
    
class Images(models.Model):
    image = models.ImageField(upload_to='product_images/image')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    
class Tag(models.Model):
    name=models.CharField(max_length=200)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    subject=models.CharField(max_length=200)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.email
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    address=models.TextField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    postcode=models.IntegerField()
    phone = models.CharField(max_length=15)
    email=models.EmailField(max_length=100)
    amount=models.CharField(max_length=120)
    payment_id=models.CharField(max_length=200,null=True,blank=True)
    paid=models.BooleanField(default=False,null=True)
    date = models.DateField(default=datetime.datetime.now)  

    
    
    def __str__(self):
     return self.user.username
 
 
 
class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    product = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/order_Img')
    quantity = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    total_price = models.CharField(max_length=200)
    
    def __str__(self):
     return self.order.user.username
 
 

class Banner(models.Model):
    title = models.CharField(max_length=100)  # Ensure the field name is correct
    category = models.CharField(max_length=50)
    price = models.CharField(max_length=20)
    image = models.ImageField(upload_to='banners/banner')

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/images')
    content = models.TextField()
    date_published = models.DateField()

    def __str__(self):
        return self.title
