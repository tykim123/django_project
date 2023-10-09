from django.db import models
from django.utils import timezone

from django.core import validators


# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()


# class Board(models.Model):
#     id = models.AutoField(primary_key = True)
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     content = models.TextField()
#     create_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

class Board(models.Model):
    id = models.AutoField(primary_key=True)  # integer(auto-increment)

    title = models.CharField("제목", max_length=255,  # varchar(255)
                             validators=[
                                 validators.MinLengthValidator(2, "최소 세 글자 이상은 입력해주셔야 합니다.")
                             ])
    author = models.CharField(max_length=255)
    content = models.TextField(validators=[
        validators.MinLengthValidator(10, "최소 10글자 이상은 입력해주셔야 합니다."),
    ])  # Text
    create_at = models.DateTimeField(auto_now_add=True)  # 추가될 때 default로 현재시간
    updated_at = models.DateTimeField(auto_now=True)  # 추가or업데이트 될 때 default로 현재시간


class Comment(models.Model):
    id = models.AutoField(primary_key=True)  # board의 프라이머리키로 연결
    content = models.CharField(max_length=255)  # varchar(255) 로 설정하여 charfield 사용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    board = models.ForeignKey('Board', on_delete=models.SET_NULL, null=True)
    # board = models.ForeignKey(Board, on_delete=models.CASCADE)
