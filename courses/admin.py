from django.contrib import admin
import lernado.courses as courses

admin.site.register(courses.models.Course)
admin.site.register(courses.models.CoursePage)
admin.site.register(courses.models.Question)
admin.site.register(courses.models.QuestionVisit)
admin.site.register(courses.models.Answer)
admin.site.register(courses.models.Activity)
admin.site.register(courses.models.ActivityResponse)
admin.site.register(courses.models.ActivityResponseVisit)
