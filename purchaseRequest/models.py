import datetime
from django.db import models


class PurchaseRequest(models.Model):
    """请购单 """

    PRQ_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批'),
        (2, '已关闭')
    )
    id = models.AutoField(primary_key=True)
    prq_identify = models.CharField(max_length=15, verbose_name='请购单编号')
    prq_serial = models.CharField(max_length=4, verbose_name='请购单流水')
    organization = models.ForeignKey('base.Organization', related_name='org_prq', verbose_name='组织', on_delete=models.CASCADE)
    prq_type = models.CharField(max_length=20, verbose_name='需求类型')
    material_type = models.ForeignKey('base.MaterialType', verbose_name='物料类别', on_delete=models.CASCADE)
    prq_department = models.CharField(max_length=20, verbose_name='请购部门')
    prq_date = models.DateTimeField(default=datetime.datetime.now, verbose_name='请购日期')
    prq_remarks = models.TextField(max_length=400, verbose_name='请购备注', null=True)
    prq_status = models.IntegerField(choices=PRQ_STATUS_CHOICES, verbose_name='请购状态')
    prq_creator = models.CharField(max_length=20, verbose_name='请购创建名字')
    prq_creator_identify = models.CharField(max_length=20, verbose_name="请购单创建者工号")
    prq_created_at = models.DateTimeField(auto_now_add=True, verbose_name='请购创建时间')
    prq_closer = models.CharField(max_length=20, verbose_name='请购关闭者', null=True)
    prq_closer_identify = models.CharField(max_length=20, verbose_name='请购关闭者工号', null=True)
    prq_closed_at = models.DateTimeField(auto_now_add=True, verbose_name='请购关闭时间', null=True)
    prq_closeReason = models.TextField(max_length=200, verbose_name='请购关闭原因', null=True)

    class Meta:
        db_table = 'db_purchase_request'
        verbose_name = "请购单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.prq_identify


class PurchaseRequestDetail(models.Model):
    """请购单物料明细"""
    # 这里还没完善，需要建立与物料库存的关系
    PRD_USE_STATUS_CHOICES = (
        (0, '未使用'),
        (1, '已使用')
    )
    id = models.AutoField(primary_key=True)
    prq_identify = models.CharField(max_length=15,verbose_name="请购单编号")
    purchase_request = models.ForeignKey('PurchaseRequest', related_name='prq_prqd', verbose_name='请购单', on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_prqd', on_delete=models.CASCADE)  # attention
    prqd_num = models.IntegerField(verbose_name='请购数量')
    prqd_present_num = models.IntegerField(verbose_name='现存量')
    prqd_remarks = models.TextField(max_length=400, verbose_name='物料请购备注', null=True)
    prqd_used = models.IntegerField(choices=PRD_USE_STATUS_CHOICES, verbose_name='明细单是否使用')

    class Meta:
        db_table = 'db_purchase_request_detail'
        verbose_name = "请购单物料明细"
        verbose_name_plural = verbose_name
