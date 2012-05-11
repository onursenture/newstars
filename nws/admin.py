from django.contrib import admin
from newstars.nws.models import *

class IAdmin(admin.ModelAdmin): pass
admin.site.register(Instructor,IAdmin)

class StAdmin(admin.ModelAdmin): pass
admin.site.register(Student,StAdmin)

class CAdmin(admin.ModelAdmin): pass
admin.site.register(Course,CAdmin)

class SeAdmin(admin.ModelAdmin): pass
admin.site.register(Section,SeAdmin)

class ScAdmin(admin.ModelAdmin): pass
admin.site.register(Schedule,ScAdmin)

class DAdmin(admin.ModelAdmin): pass
admin.site.register(Department,DAdmin)

class EAdmin(admin.ModelAdmin): pass
admin.site.register(Enrollment,EAdmin)
