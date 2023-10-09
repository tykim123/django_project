from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name = "index"),
    path('<int:board_id>/', views.board_detail, name = 'detail'),
    path('write/', views.board_write, name='write'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_list, name='question_create'),


    # path('<int:board_id>/',
    #      views.board_detail,
    #      name = "board_detail"),
    path('comments/',
         views.comment_list,
         name = "comment_list"),
]

#     path('board/', views.board_list, name='board_list'),
#     path('comments/', views.comment_list, name='comment_list'),
#     path('question/', views.question_list, name='question_list'),
# ]