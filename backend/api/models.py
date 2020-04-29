from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
import uuid, datetime
import os

# User model based on AbstractUser, the default user.
class User(AbstractUser):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=200)
    role = models.CharField(max_length=200, default='Client')
    created_on = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    address = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.uid) + " - " + self.role + " - " + " - " + self.email

def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join('documents/', filename)

class DeclarationType(models.Model):
    dtid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.dtid) + " - " + self.name + " - " + str(self.created_on)

class Declaration(models.Model):
    did = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    address = models.CharField(max_length=200)
    geo_cord = models.CharField(max_length=200)
    citizen = models.ForeignKey(get_user_model(), related_name='declarations',on_delete=models.CASCADE)
    states = [
        ('not_validated', 'not_validated'),
        ('lack_of_info', 'lack_of_info'),
        ('validated', 'validated'),
        ('refused', 'refused'),
        ('under_treatment', 'under_treatment'),
        ('treated', 'treated'),
        ('archived', 'archived'),
    ]
    status = models.CharField(max_length=200, choices=states, default='not_validated')
    dtype = models.ForeignKey(DeclarationType, related_name='declarations',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    validated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.did) + " - " + self.title + " - " + str(self.created_on)

class DeclarationRejection(models.Model):
    drid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    maire = models.ForeignKey(get_user_model(), related_name='declarations_rejections',on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    declaration = models.OneToOneField(Declaration, related_name='rejection', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.drid) + " - " + self.reason + " - " + str(self.created_on)

class DeclarationComplementDemand(models.Model):
    dcid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    maire = models.ForeignKey(get_user_model(), related_name='declarations_complement_demands',on_delete=models.CASCADE)
    declaration = models.ForeignKey(Declaration, related_name='complement_demands', on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.dcid) + " - " + self.reason + " - " + str(self.created_on)

class Document(models.Model):
    dmid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    DocumentType = [
        ('pdf', 'pdf'),
        ('image', 'image'),
        ('other', 'other'),
    ]
    filetype = models.CharField(max_length=200, choices=DocumentType ,default='other')
    src = models.FileField(upload_to=wrapper)
    declaration = models.ForeignKey(Declaration, related_name='attachments',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.dmid) + " - " + self.filetype + " - " + str(self.created_on)

class Report(models.Model):
    rid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    declaration = models.OneToOneField(Declaration, related_name='report', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    service = models.ForeignKey(get_user_model(), related_name='reports',on_delete=models.CASCADE)
    states = [
        ('not_validated', 'not_validated'),
        ('lack_of_info', 'lack_of_info'),
        ('work_not_finished', 'work_not_finished'),
        ('validated', 'validated'),
        ('refused', 'refused'),
        ('archived', 'archived'),
    ]
    status = models.CharField(max_length=200, choices=states, default='not_validated')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    validated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.rid) + " - " + self.title + " - " + str(self.created_on)

class ReportRejection(models.Model):
    rrid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    maire = models.ForeignKey(get_user_model(), related_name='reports_rejections',on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    report = models.OneToOneField(Report, related_name='rejection', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rrid) + " - " + self.reason + " - " + str(self.created_on)

class ReportComplementDemand(models.Model):
    rcid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    maire = models.ForeignKey(get_user_model(), related_name='reports_complement_demands',on_delete=models.CASCADE)
    report = models.ForeignKey(Report, related_name='complement_demands', on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rcid) + " - " + self.reason + " - " + str(self.created_on)

class Announce(models.Model):
    aid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    states = [
        ('published', 'published'),
        ('modified', 'modified'),
        ('removed', 'removed'),
        ('archived', 'archived'),
    ]
    status = models.CharField(max_length=200, choices=states, default='published')
    created_on = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def __str__(self):
        return str(self.aid) + " - " + self.title + " - " + str(self.created_on)