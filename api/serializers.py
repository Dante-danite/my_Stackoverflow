from djoser.serializers import UserSerializer
from rest_framework import serializers
from aplication.models import *
from djoser.serializers import UserSerializer

class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        author = validated_data.pop('author')
        text = validated_data.pop('text')
        try:
            answer_id = validated_data.pop('answer')
            comment = Comment.objects.create(author=author, text=text, answer=answer_id)
        except KeyError:
            question_id = validated_data.pop('question')
            comment = Comment.objects.create(author=author, text=text, question=question_id)
        return comment

    def update(self, instance, validated_data):
        text = validated_data.pop('text')
        if instance.author.id == validated_data['author'].id:
            try:
                answer_id = validated_data.pop('answer')
                if answer_id == instance.answer:
                    instance.text = text
                    instance.save()
                else:
                    raise serializers.ValidationError('У данного пользователя нет комментария к этому ответу')
            except KeyError:
                question_id = validated_data.pop('question')
                if question_id == instance.question:
                    instance.text = text
                    instance.save()
                else:
                    raise serializers.ValidationError('У данного пользователя нет комментария к этому вопросу')
        else:
            raise serializers.ValidationError('Неверный пользователь')
        return instance

class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data['title']
        if Tag.objects.filter(title=title).exists():
            raise serializers.ValidationError('Данный тег существует')
        tag = Tag.objects.create(title=title)
        return tag

    def update(self, instance, validated_data):
        title = validated_data.get('title', instance.title)
        if title != instance.title and Tag.objects.filter(title=title).exists():
            raise serializers.ValidationError('Данный тег существует')
        instance.title = title
        instance.save()
        return instance


class AnswerListSerializer(serializers.ModelSerializer):
    comments_answer = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        author = validated_data.pop('author')
        text = validated_data.pop('text')
        question_id = validated_data.pop('question')
        answer = Answer.objects.create(author=author, text=text, question=question_id)
        return answer

    def update(self, instance, validated_data):
        text = validated_data.pop('text')
        if instance.author.id == validated_data['author'].id:
            if instance.question.id == validated_data['question'].id:
                instance.text = text
                instance.save()
            else:
                raise serializers.ValidationError('У пользователя нет ответа на данный вопрос')

        else:
            raise serializers.ValidationError('Неверный пользователь')
        return instance

class QuestionListSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True)
    answers = AnswerListSerializer(many=True, read_only=True)
    comments_question = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        author = validated_data.pop('author')
        question = Question.objects.create(author=author, **validated_data)

        for tag_data in tags_data:
            tag_title = tag_data.get('title')
            tag, created = Tag.objects.get_or_create(title=tag_title)
            question.tags.add(tag)
        return question

    def update(self, instance, validated_data):
        if instance.author.id == validated_data["author"].id:
            instance.title = validated_data["title"]
            instance.text = validated_data["text"]
            tags_data = validated_data.pop('tags', None)
            if tags_data is not None:
                instance.tags.clear()
                for tag_data in tags_data:
                    tag_title = tag_data.get('title')
                    tag, created = Tag.objects.get_or_create(title=tag_title)
                    instance.tags.add(tag)
            instance.save()
        else:
            raise serializers.ValidationError('Неверный пользователь')
        return instance
