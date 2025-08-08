from django.db import models
import uuid, secrets
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    ROLE_CHOICE = [('owner', 'Owner'), ('employee', 'Employee')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICE)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, password):
        self.password_hash = make_password(password) 

    def check_password(self, password):
        return check_password(password, self.password_hash)

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False


class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auth_tokens")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_token():
        return secrets.token_hex(32) 
