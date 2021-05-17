from django.contrib import admin
from store.models import Collection,Order,OrderItem,Product,Cart,CartItem
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','stock','created','updated']
    list_editable=['price','stock']
    list_per_page=5

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','name','email','total','token',]
    list_per_page=5

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order','product','quantity','price',]
    list_per_page=5

admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
