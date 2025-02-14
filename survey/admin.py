from django.contrib import admin

from survey.models import Choice, Survey ,Answer ,Question,Response

# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Response)
admin.site.register(Answer)