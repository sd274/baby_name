from django.contrib import admin
from .models import BabyName, Reaction, UserNameReaction

# Register your models here.
admin.site.register([
    BabyName,
    Reaction,
    UserNameReaction

])
