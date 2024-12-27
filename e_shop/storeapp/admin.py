from django.contrib import admin
from .models import *

class ImagesTabularInline(admin.TabularInline):
    model =Images 
    
    
class TagTabularInline(admin.TabularInline):
    model =Tag
    
class ProductAdmin(admin.ModelAdmin):
    inlines=[ImagesTabularInline,TagTabularInline]
    
    
class OrderItemTabular(admin.TabularInline):
    model=OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemTabular]
    list_display=['firstname','phone','email','payment_id','paid','date']
    search_fields=['firstname','email','paymentn_id']


# Register your models here.
admin.site.register(Images)
admin.site.register(Tag)



admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_price)
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)

#for Banner
admin.site.register(Banner)

#for blog:
admin.site.register(Blog)

