from questionnaire.models import Alternative, Answer, Label, Question

from django.contrib import admin

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Alternative)
admin.site.register(Label)
