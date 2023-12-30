from django.contrib import admin
from django.contrib import admin
from .models import Phishing, Form, Input, Action

# Register your models here.
admin.site.register(Phishing)
admin.site.register(Form)
admin.site.register(Input)
admin.site.register(Action)
