from django.contrib import admin
from .models import *


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    readonly_fields = ('date_create', 'date_update')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(FavoritQuestion)
admin.site.register(FavoritAnswer)
admin.site.register(VoiceQuestion)
admin.site.register(VoiceAnswer)
admin.site.register(Comment)
