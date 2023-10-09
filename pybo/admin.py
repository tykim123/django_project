from django.contrib import admin
from .models import Question, Board, Comment

# Register your models here.
admin.site.register(Question)
admin.site.register(Board)
admin.site.register(Comment)


