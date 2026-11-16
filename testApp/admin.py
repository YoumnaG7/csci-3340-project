from django.contrib import admin
from .models import Event, ShareAccess

# Register your models here.

admin.site.Register(Event)
admin.site.Register(ShareAccess)
