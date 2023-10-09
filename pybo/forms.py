from django import forms
from pybo.models import Board, Comment


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Board  # 사용할 모델
        fields = ['title', 'content']  # QuestionForm에서 사용할 보드 모델의 속성
        widgets = {
                    'title': forms.TextInput(attrs={'class': 'form-control'}),
                    'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
                }
        labels = {
            'title': '제목',
            'content': '내용',
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]



class BoardForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget_update()
        # self.a = #public
        # self._a = #protected
        # self.__a = #private

    class Meta:
        model = Board
        fields = ["title", "content", 'author']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': "제목을 입력해 주세요."
                }
            )
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'author' : '작성자'
        }

    # def sample(self):
    #     self.__private_sample()
    #     pass
    #
    # def __private__sample(self):
    #     pass

    def _widget_update(self):
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
