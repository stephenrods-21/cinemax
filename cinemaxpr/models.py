from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class businessunit(models.Model):
    name = models.CharField(max_length=75, null=False)
    prefix = models.CharField(max_length=25, null=False)
    documentno = models.IntegerField(default=1000)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=75, null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ExtendedUser(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    businessunit = models.ForeignKey(businessunit, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)


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
    level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)


class ApprovalStatus(models.Model):
    name = models.CharField(max_length=75, null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Memo(models.Model):
    documentno = models.CharField(max_length=50, null=False)
    topic = models.CharField(max_length=500, null=False)
    businessunit = models.ForeignKey(businessunit, on_delete=models.CASCADE)
    approvalstatus = models.ForeignKey(
        ApprovalStatus, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    deadline_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic
