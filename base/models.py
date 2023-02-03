from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.contrib.postgres.indexes import GinIndex
# Create your models here.

class Parishe(models.Model):
    parish_name=models.CharField(max_length=255)
    county_located_in=models.CharField(max_length=255,null=True)
    coordinates=models.CharField(max_length=500)
    perimeter=models.FloatField(blank=True)
    pop_199=models.FloatField(blank=True)
    total_area=models.FloatField(blank=True)
    area=models.FloatField(blank=True)
    count=models.FloatField(blank=True)
    acres=models.FloatField(blank=True)
    area_km=models.FloatField(blank=True)
    pop_200=models.FloatField(blank=True)
   

class Countie(models.Model):
    county_name=models.CharField(max_length=255)
    parishes_in_county=models.CharField(max_length=255,blank=True)

class Address(models.Model):
    address=models.CharField(max_length=1000)
    post_code=models.CharField(max_length=255,blank=True,null=True)
    latitude=models.FloatField()
    longitude=models.FloatField()
    source=models.CharField(max_length=255,blank=True,null=True)
    comm_poij=models.CharField(max_length=1000,blank=True,null=True)
    category=models.CharField(max_length=255,blank=True,null=True)
    dev_area=models.CharField(max_length=1000,blank=True,null=True)
    parish=models.CharField(max_length=255,blank=True,null=True)
    comm_sdc=models.CharField(max_length=1000,blank=True,null=True)
    settlement=models.CharField(max_length=1000,blank=True,null=True)
    name=models.CharField(max_length=1000,blank=True,null=True)
    
    class Meta:
        indexes=[
            GinIndex(name='aIndex',fields=['address'],opclasses=['gin_trgm_ops']),
            GinIndex(name='nIndex',fields=['name'],opclasses=['gin_trgm_ops']),
            GinIndex(name='pIndex',fields=['parish'],opclasses=['gin_trgm_ops']),
            GinIndex(name='dIndex',fields=['dev_area'],opclasses=['gin_trgm_ops']),
            GinIndex(name='cIndex',fields=['comm_sdc'],opclasses=['gin_trgm_ops'])
        ]


class CustomUserManager(BaseUserManager):
    def _create_user(self,first_name,last_name,email,password,**extrafields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Password is not provided')
   
        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            **extrafields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,first_name,last_name,email,password,**extra_fields):
       extra_fields.setdefault('is_staff',True)
       extra_fields.setdefault('is_active',True)
       extra_fields.setdefault('is_superuser',False)
       return self._create_user(first_name,last_name,email,password,**extra_fields)

    def create_superuser(self,first_name,last_name,email,password,**extra_fields):
       extra_fields.setdefault('is_staff',True)
       extra_fields.setdefault('is_active',True)
       extra_fields.setdefault('is_superuser',True)
       return self._create_user(first_name,last_name,email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(db_index=True,max_length=255,unique=True)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
   

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    
    objects=CustomUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']

    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'


class ResourceRouter(models.Model):
    specs=models.FileField(upload_to=("Address"))
