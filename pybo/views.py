from django.shortcuts import render, redirect  # HTML를 렌더링한다.
from django.http import HttpResponse
from .models import Board, Comment, Question, Answer
from django.utils import timezone
from .forms import QuestionForm
from django.core.paginator import Paginator
from django.urls import reverse
#TODO:
"""
1. board detail에서댓글을달수있는form태그와 input tag만들기

2.form이 submit되면요청을받을url과 view function만들기
    -1.form에입력값이빈값이면， error를담아서html1보내기
    -2.form에입력값이타당하면，저장하고상세페이지다시보여주기
    
3.(2)에서만들어진ur1로(1)의form에 action속성에ur1기록하기
"""



def index(request):
    page = request.GET.get('page', '1')  # 페이지
    board_list = Board.objects.prefetch_related('comment_set').all()

    paginator = Paginator(board_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'board_list': page_obj}
    return render(request, 'board/index.html', context)


# # Create your views here.
# def index(request):
#     sample_list = Question.objects.all()
#     return render(request, 'board/index.html', {'name' : '유저', 'sample':sample_list})
"""board_list라는 view함수를 만들고 /board 로 접속하면
게시글에 대한 전체 게시글을 리스트(HTML:ul, li 태그 이용)로 보여주세요."""


def board_list(request):
    qs = Board.objects.all()

    html = ""
    for board in qs:
        html += "<li>{board.title}</li>"
    html = f"<ul>{html}</ul>"
    return HttpResponse(html)


"""/board/commnets로 접속하면 모든 댓글을 조회하도록 조회내용 형식
ppt 참고"""


def comment_list(request):
    qs = Comment.objects.all()

    html = ""

    for comment in qs:
        html += f"<li>{comment.id} | \
                   {comment.content} | {comment.board_id} </li>"

    html += f"<ul>{html}</ul>"

    return HttpResponse(html)



from .forms import CommentForm

def board_detail(request, board_id):
    board = Board.objects.get(pk=board_id)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleanded_data
            Comment(
                content = data['content'],
                board_id=board_id
            ).save()
            return redirect(reverse('pybo:detail',
                                    kwargs={'board_id': board_id}))




"""
폼사용하지 않고 댓글 다는 코드
"""
def board_detail(request, board_id):
    errors = []
    if request.method == 'POST':
        data = request.POST
        content = data.get('comment')
        if content:
            comment = Comment(
                content=content,
                board_id=board_id
            )
            comment.save()
        else:
            errors.append("comment가 비어 있습니다.")

    board = Board.objects.get(pk=board_id)

    return render(request,
                  "board/detail.html",
                  {'board': board, 'errors': errors})







def board_detail(request, board_id):
    board = Board.objects.get(pk=board_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:  # 댓글이 비어있지 않은 경우에만 추가
            Comment.objects.create(board=board, content=content)
            # 댓글 추가 후에는 같은 페이지로 리다이렉트
            return redirect('pybo:detail', board_id=board.id)
    return render(request,
                  "board/detail.html",
                  {'board': board})



# def board_detail(request, board_id):
#     qs = Board.objects.get(id = board_id)
#     comment_list = qs.commnet_set.all()
#
#     html = f"<h1>{qs.title}</h1> \
#         <div>{qs.content}</div>"
#
#     html += "<ul>"
#     for comment in comment_list:
#         html += f"<li>{comment.content}</li>"
#     html += "</ul>"
#
#     return HttpResponse(html)


def question_list(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id=question.id)


# def board_write(request):
#     if request.method == 'POST':

#         form = write(request.POST)
#         if form.is_valid():
#             board = form.save(commit=False)
#             board.create_at = timezone.now()
#             board.save()
#             return redirect('pybo:index')
#     else:
#         form = QuestionForm()
#
#     return render(request, 'board/write.html')

from .forms import BoardForm


#
# def board_write(request):
#     if request.method == 'POST':
#         # #save the model
#         data = request.POST
#         title = data.get('title')
#         content = data.get('content')
#         board = Board(
#             title=title,
#             content = content,
#             author=request.user
#         )
#         board.save()
#     ##문제 x -> index페이지
#         return redirect(reverse('pybo:index'))
#     return render(request,
#                   "board/write.html")
#     ##에러 발생 -> 에러 랜더링





def board_write(request):
    form = BoardForm()
    if request.method == 'POST':
        if form.is_valid():
            board = form.save(commit=False)
            board.create_at = timezone.now()
            form.save()
            return redirect('pybo:index')
        else:
            form = BoardForm()
    return render(request, 'board/write.html',
                  {'form': form})


def comment_create(request, board_id):
    board = Board.objects.get(pk=board_id)

    if request.method == 'POST':
        content = request.POST.get('content')  # 댓글 내용을 가져옴
        Comment.objects.create(board=board, content=content)
    return redirect('pybo:detail', board_id=board.id)
