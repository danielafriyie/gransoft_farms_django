from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

User = settings.AUTH_USER_MODEL


class UsersManager(BaseUserManager):

    def create_user(self, username, name, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        username = self.model.normalize_username(username)
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, **extra_fields):
        user = self.create_user(username=username, name=name, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_immutable = True
        user.save(using=self._db)
        return user


class BaseUserAccountsModel(models.Model):
    gender_category = (
        ('Male', 'Male'), ('Female', 'Female')
    )
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=gender_category)
    date_of_birth = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_immutable = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class UserAccountsModel(AbstractBaseUser, PermissionsMixin):
    gender_category = (
        ('Male', 'Male'), ('Female', 'Female')
    )

    username = models.CharField(max_length=35, unique=True)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=gender_category)
    date_of_birth = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_immutable = models.BooleanField(default=False)
    auth_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.RESTRICT)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone_no', 'gender', 'date_of_birth', 'auth_user']

    objects = UsersManager()

    class Meta:
        permissions = (
            ('add_user', 'Can add user'),
            ('update_user', 'Can update user'),
            ('delete_user', 'Can delete user'),
        )
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        db_table = 'user_accounts_model'


class UserAccountsModelAudit(BaseUserAccountsModel):
    username = models.CharField(max_length=35)
    auth_user = models.IntegerField(null=True, blank=True)
    action_flag = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'User Account Audit'
        verbose_name_plural = 'User Accounts Audit'
        db_table = 'user_accounts_model_audit'


class UsersAuthenticationLog(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'User Authentication Log'
        verbose_name_plural = 'Users Authentication Log'
        db_table = 'users_authentication_log'
