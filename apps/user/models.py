from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from apps.role.models import AccessRole
from common.models import BaseModel
from apps.company.models import Company


class MyUserManager(BaseUserManager):
    """The Custom BaseManager Class"""

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email
        """
        user = self.create_user(email, password=password)
        user.is_super_user = True
        user.is_company_owner = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    """
    User model with email and password as a login credentials
    """

    full_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=False, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(
        AccessRole, on_delete=models.SET_NULL, null=True, blank=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_super_user = models.BooleanField(default=False)
    is_company_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        """
        String representation of name
        :return:
        """
        return "{}-{}--{}".format(self.email, self.id, self.role)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    class Meta:
        """
        Verbose name and verbose plural
        """

        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        unique_together = ("role", "email")
        get_latest_by = "created_at"

    """
    To create a new instance of User model
    """
