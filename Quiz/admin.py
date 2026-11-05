from django.contrib import admin
from .models import Option, Participant, Question, Quiz

# Register your models here.
class OptionInline(admin.TabularInline):
  model = Option
  extra = 4


class QuestionAdmin(admin.ModelAdmin):
  inlines = [OptionInline]


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Participant)