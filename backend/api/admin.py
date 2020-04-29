from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Declaration)
admin.site.register(DeclarationType)
admin.site.register(DeclarationRejection)
admin.site.register(DeclarationComplementDemand)
admin.site.register(Document)
admin.site.register(Report)
admin.site.register(ReportRejection)
admin.site.register(ReportComplementDemand)
admin.site.register(Announce)