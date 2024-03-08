from django.db import models
import uuid
from master.models import *

# Create your models here.
class Van(models.Model):
    van_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    van_make = models.CharField(max_length=50)
    plate = models.CharField(max_length=50)
    renewal_date = models.DateTimeField(blank=True, null=True)
    insurance_expiry_date = models.DateTimeField(blank=True, null=True)
    capacity = models.IntegerField(null=True, blank=True)
    driver = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='driver_van', limit_choices_to={'user_type': 'Driver'})
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='salesman_van', limit_choices_to={'user_type': 'Salesman'})
    branch_id = models.ForeignKey('master.BranchMaster', on_delete=models.SET_NULL, null=True, blank=True, related_name='van_branch')


    class Meta:
        ordering = ('van_make',)

    def __str__(self):
        return str(self.van_make)
    
class Van_Routes(models.Model):
    van_route_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    van = models.ForeignKey(Van, on_delete=models.SET_NULL, null=True, blank=True,related_name='van_master')
    routes = models.ForeignKey(RouteMaster, on_delete=models.SET_NULL, null=True, blank=True,related_name='van_routes')

    class Meta:
        ordering = ('van',)

    def __str__(self):
        return str(self.van)

class Van_License(models.Model):
    van_license_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    van = models.ForeignKey(Van, on_delete=models.SET_NULL, null=True, blank=True,related_name='van_license')
    emirate = models.ForeignKey(EmirateMaster, on_delete=models.SET_NULL, null=True, blank=True,related_name='license_emirate')
    license_no = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('van',)

    def __str__(self):
        return str(self.van)