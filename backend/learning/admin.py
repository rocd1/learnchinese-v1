from django.contrib import admin
from learning.models import * 


# Register your models here.
admin.site.register(HSKLevel)
admin.site.register(Vocabulary)
admin.site.register(Lesson)
admin.site.register(GrammarPoint)
admin.site.register(Character)
admin.site.register(ExampleSentence)
admin.site.register(LearnedWord)
admin.site.register(QuizResult)
admin.site.register(QuizAnswer)
admin.site.register(FavoriteWord)