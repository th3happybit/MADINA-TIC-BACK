from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager, PermissionsMixin
import uuid, datetime
import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=settings.EMAIL_HOST_USER, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

def wrapperuser(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join('images/', filename)

# User model based on AbstractUser, the default user.
class User(AbstractUser):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=200)
    roles = [
        ('Client', 'Client'),
        ('Admin', 'Admin'),
        ('Maire', 'Maire'),
        ('Service', 'Service'),
    ]
    role = models.CharField(max_length=200, choices=roles, default='Client')
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to=wrapperuser, blank=True, null=True)
    is_approved = models.BooleanField(
        _('approved'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as approved. '
        ),
    )
    national_id = models.CharField(max_length=200, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

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
    address = models.CharField(max_length=200, blank=True, null=True)
    geo_cord = models.CharField(max_length=200, blank=True, null=True)
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
    src = models.FileField(blank=True)
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