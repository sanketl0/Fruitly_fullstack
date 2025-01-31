from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, first_name, last_name, password=None, role='user2'):
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        
        # Normalize the mobile number (if needed)
        mobile_number = self.normalize_mobile_number(mobile_number)
        
        user = self.model(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, first_name, last_name, password=None, role='admin'):
        user = self.create_user(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def normalize_mobile_number(self, mobile_number):
        """
        Normalize the mobile number by removing any non-digit characters.
        Example: +91-1234567890 -> 911234567890
        """
        return ''.join(filter(str.isdigit, mobile_number))
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user1', 'User1'),
        ('user2', 'User2'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15, unique=True)  # Mobile number field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user2')
    is_approved = models.BooleanField(default=False)  # To track approval status

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'  # Use mobile_number as the username field
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Additional required fields

    def __str__(self):
        return f'{self.first_name} {self.last_name}'  # Return mobile_number as the string representation






# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, password=None, role='user2'):
#         if not email:
#             raise ValueError('Users must have an email address')
#         email = self.normalize_email(email)
#         user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
#         user.set_password(password)
#         user.is_active = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password=None, role='admin'):
#         user = self.create_user(email, first_name, last_name, password, role=role)
#         user.is_staff = True
#         user.is_superuser = True
#         user.is_active = True
#         user.save(using=self._db)
#         return user

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('user1', 'User1'),
#         ('user2', 'User2'),
#     )

#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user2')

#     is_approved = models.BooleanField(default=False)  # To track approval status


#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def __str__(self):
#         return self.email












# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, password=None, role='user2'):
#         if not email:
#             raise ValueError('Users must have an email address')
#         email = self.normalize_email(email)
#         user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password=None, role='admin'):
#         user = self.create_user(email, first_name, last_name, password, role=role)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('user1', 'User1'),
#         ('user2', 'User2'),
#     )

#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user2')
#     is_active = models.BooleanField(default=False)
#     is_approved = models.BooleanField(default=False)  # To track approval status


#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def __str__(self):
#         return self.email
