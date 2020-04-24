from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()

email = 'oussamamessabih02@gmail.com'
password = 'blackholE'

try:
    User.objects.get(username='admin')
    print ("User 'admin' already exist")
except User.DoesNotExist:
    User.objects.create_superuser('admin', email, password)
    print ("User 'admin created with default password'")