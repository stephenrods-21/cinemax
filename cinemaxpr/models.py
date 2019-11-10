from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class businessunit(models.Model):
    name = models.CharField(max_length=75, null=False)
    prefix = models.CharField(max_length=25, null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ExtendedUser(models.Model):
    role = models.IntegerField(default=0)
    businessunit = models.OneToOneField(businessunit, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class LineOfApproval(models.Model):
    name = models.CharField(max_length=75, null=False)
    businessunit = models.ForeignKey(businessunit, on_delete=models.CASCADE)
    no_of_approver = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LineOfApprovalDetail(models.Model):
    line_of_approval = models.ForeignKey(LineOfApproval, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    must_approve = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)

