from api.models import Declaration, Report, Announce
Declaration.objects.all().delete()
Report.objects.all().delete()
Announce.objects.all().delete()
# Declaration.objects.filter(created_on__lt=datetime.now()).delete()
# Report.objects.filter(created_on__lt=datetime.now()).delete()
# Announce.objects.filter(created_on__lt=datetime.now()).delete()