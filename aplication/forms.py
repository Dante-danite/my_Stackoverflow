from django import forms
from .models import *


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ('views', 'author')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields =('text',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('question', 'author', 'status_accepted')


