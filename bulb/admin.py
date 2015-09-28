from django.contrib import admin

from bulb.models import Category, Book, Request, Point

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Request)
admin.site.register(Point)

