from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EntityType(models.Model):
    entity_name = models.CharField(max_length=50, null=False)

class businessunit(models.Model):
    name = models.CharField(max_length=75, null=False)
    prefix = models.CharField(max_length=25, null=False)
    documentno = models.IntegerField(default=1000)
    is_visible = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)

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
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)


class ExtendedUser(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    businessunit = models.ForeignKey(businessunit, blank=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=75, null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)


class LineOfApproval(models.Model):
    name = models.CharField(max_length=75, null=False)
    businessunit = models.ForeignKey(businessunit, blank=True, on_delete=models.CASCADE)
    no_of_approver = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LineOfApprovalDetail(models.Model):
    line_of_approval = models.ForeignKey(LineOfApproval, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    # must_approve = models.BooleanField(default=False)
    required_approval = models.IntegerField(null=False, default=1)
    level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)


class ApprovalStatus(models.Model):
    name = models.CharField(max_length=75, null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)

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
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)


class MemoDetail(models.Model):
    documentno = models.CharField(max_length=50, null=False)
    topic = models.CharField(max_length=500, null=False)
    businessunit = models.ForeignKey(businessunit, blank=True, on_delete=models.CASCADE)
    approvalstatus = models.ForeignKey(ApprovalStatus, on_delete=models.CASCADE)
    budget = models.ForeignKey(BudgetDetail, blank=True, null=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    deadline_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

class PurchaseRequisitionDetail(models.Model):
    title = models.CharField(max_length=150, null=False)
    budgetDetail = models.ForeignKey(BudgetDetail, on_delete=models.CASCADE)
    status = models.ForeignKey(ApprovalStatus, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deadline_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)

class TransactionDetail(models.Model):
    level = models.IntegerField(null=False, default=1)
    extendeduserObj = models.IntegerField(null=False, default=1)
    transactionstatus = models.IntegerField(null=False, default=1)
    required_approval = models.IntegerField(null=False, default=1)
    lineOfApprovalObj = models.IntegerField(null=False, default=0)
    businessunitObj = models.IntegerField(blank=True, null=True)
    memoObj = models.ForeignKey(MemoDetail, blank=True, null=True, on_delete=models.CASCADE)
    purchaseRequisitionDetail = models.ForeignKey(PurchaseRequisitionDetail, blank=True, null=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    entity_type = models.ForeignKey(EntityType, default=1, on_delete=models.CASCADE)

