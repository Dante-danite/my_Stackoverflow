from django import forms

from .models import *


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ('views', 'author')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
