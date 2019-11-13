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

class BudgetDetail(models.Model):
    description = models.CharField(max_length=500, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class MemoDetail(models.Model):
    documentno = models.CharField(max_length=50, null=False)
    topic = models.CharField(max_length=500, null=False)
    businessunit = models.ForeignKey(businessunit, on_delete=models.CASCADE)
    approvalstatus = models.ForeignKey(ApprovalStatus, on_delete=models.CASCADE)
    budget = models.ForeignKey(BudgetDetail, blank=True, null=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    deadline_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

class TransactionDetail(models.Model):
    level = models.IntegerField(null=False, default=1)
    extendeduser = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    must_approve = models.BooleanField(default=False)
    transactionstatus = models.IntegerField(null=False, default=1)
    lineOfApproval = models.IntegerField(null=False, default=0)
    businessunit = models.IntegerField(null=False, default=1)
    memo = models.IntegerField(null=False, default=1)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)

