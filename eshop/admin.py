from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(SizeProductMAp)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Payment)
admin.site.register(ContactUs)
admin.site.register(Review)
