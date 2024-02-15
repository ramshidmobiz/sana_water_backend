from django.db import models
from django.db import models
import uuid
from datetime import datetime

# Create your models here.

COUPON_METHOD_CHOICES = (
    ('digital', 'Digital'),
    ('manual', 'Manual'),
)

class CouponType(models.Model):
    coupon_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_type_name = models.CharField(max_length=20, null=True, blank=True)
    no_of_leaflets = models.CharField(max_length=20, null=True, blank=True)
    valuable_leaflets = models.CharField(max_length=20, null=True, blank=True)
    free_leaflets = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        ordering = ('coupon_type_name',)

    def __str__(self):
        return str(self.coupon_type_name)


class Coupon(models.Model):
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_type_id= models.ForeignKey(CouponType, on_delete=models.SET_NULL, null=True, blank=True,related_name='coupon_type')
    book_num = models.CharField(max_length=20, null=True, blank=True)
    value_starting_no = models.CharField(max_length=20, null=True, blank=True)
    value_ending_no = models.CharField(max_length=20, null=True, blank=True)
    free_starting_no = models.CharField(max_length=20, null=True, blank=True)
    free_ending_no = models.CharField(max_length=20, null=True, blank=True)
    branch_id = models.ForeignKey('master.BranchMaster', on_delete=models.SET_NULL, null=True, blank=True,related_name='user_login')
    status = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    coupon_method = models.CharField(max_length=10,choices=COUPON_METHOD_CHOICES,default='digital',null=True,blank=True)


    class Meta:
        ordering = ('book_num',)

    def __str__(self):
        return str(self.book_num)
    
class CouponRequest(models.Model):
    coupon_request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.CharField(max_length=20, null=True, blank=True)
    coupon_type_id= models.ForeignKey(CouponType, on_delete=models.SET_NULL, null=True, blank=True,related_name='coupon_request')
    branch_id = models.ForeignKey('master.BranchMaster', on_delete=models.SET_NULL, null=True, blank=True,related_name='branch_user')
    status = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return str(self.coupon_type_id)
    

class AssignStaffCoupon(models.Model):
    assign_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_request = models.ForeignKey(CouponRequest, on_delete=models.SET_NULL, null=True, blank=True,related_name='coupon_request_request')
    alloted_quantity = models.CharField(max_length=20, null=True, blank=True)
    remaining_quantity = models.CharField(max_length=20, null=True, blank=True)
    R_STATUS = (
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
       
    )
    status = models.CharField(max_length=20, choices=R_STATUS, null=True, blank=True)
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created_date',)
    def __str__(self):
        return str(self.assign_id)

class AssignStaffCouponDetails(models.Model):
    assign_coupon_details_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_coupon_assign = models.ForeignKey(AssignStaffCoupon, on_delete=models.SET_NULL, null=True, blank=True,related_name='assign_staff_coupon_request')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True,related_name='id_coupon')
    C_STATUS = (
        ('Pending', 'Pending'),
        ('Assigned to Staff', 'Assigned to Staff'),
        ('Assigned To Customer','Assigned To Customer')
    )
    status = models.CharField(max_length=20, choices=C_STATUS, null=True, blank=True)
    to_customer  = models.ForeignKey('accounts.Customers', on_delete=models.SET_NULL, null=True, blank=True,related_name='coupon_customer')
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return str(self.assign_coupon_details_id)
    
#--------------NewCoupon-----------------
class NewCoupon(models.Model):
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_type = models.ForeignKey(CouponType, on_delete=models.CASCADE, related_name='couponsType')
    book_num = models.CharField(max_length=20, null=True, blank=True)
    no_of_leaflets = models.CharField(max_length=20, null=True, blank=True)
    valuable_leaflets = models.CharField(max_length=20, null=True, blank=True)
    free_leaflets = models.CharField(max_length=20, null=True, blank=True)    
    branch_id = models.ForeignKey('master.BranchMaster', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_login_id')
    status = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('book_num',)

    def __str__(self):
        return str(self.book_num)
    
class CouponLeaflet(models.Model):
    couponleaflet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(NewCoupon, on_delete=models.CASCADE, related_name='leaflets')
    leaflet_number = models.CharField(max_length=10)
    used = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ('leaflet_number',)
    def __str__(self):
        return f"{self.coupon.book_num} - Leaflet {self.leaflet_number}"