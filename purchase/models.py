import datetime
from django.db import models


class PurchaseContract(models.Model):
    """采购合同"""
    PC_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )

    id = models.AutoField(primary_key=True)
    pc_identify = models.CharField(max_length=15, verbose_name='合同编号')
    pc_serial = models.CharField(max_length=4, verbose_name='合同流水号')
    organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='org_pc', on_delete=models.CASCADE)
    pc_name = models.CharField(max_length=20, verbose_name='合同名称')
    supplier = models.ForeignKey('base.Supplier', verbose_name='供应商', related_name='supplier_pc', on_delete=models.CASCADE)
    pc_date = models.DateTimeField(default=datetime.datetime.now, verbose_name='合同签订日期')
    pc_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='合同总额')
    pc_remarks = models.TextField(max_length=400, verbose_name='合同备注', null=True)
    pc_status = models.IntegerField(choices=PC_STATUS_CHOICES, default=0, verbose_name='合同状态')
    pc_creator = models.CharField(max_length=20, verbose_name='合同创建者名字')
    pc_creator_identify = models.CharField(max_length=20, verbose_name='合同创建者工号')
    pc_created_at= models.DateTimeField(auto_now_add=True, verbose_name='合同创建时间')

    class Meta:
        db_table = 'db_purchase_contract'
        verbose_name = "采购合同"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pc_name


class PurchaseContractDetail(models.Model):
    """合同物料明细"""
    PCD_USE_STATUS_CHOICES = (
        (0, '未使用'),
        (1, '已使用')
    )
    id = models.AutoField(primary_key=True)
    purchase_contract = models.ForeignKey('PurchaseContract', verbose_name='采购合同', related_name='pc_pcd', on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_pcd', on_delete=models.CASCADE)
    pcd_num = models.IntegerField(verbose_name='物料数量')
    pcd_taxRate = models.IntegerField(default=13, verbose_name='税率', null=True)
    pcd_tax_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税单价', null=True)
    pcd_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价', null=True)
    pcd_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税总额', null=True)
    pcd_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额', null=True)
    pcd_tax_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='税额', null=True)
    pcd_pr_identify = models.CharField(max_length=15, verbose_name='请购单编号')
    pcd_prd_remarks = models.TextField(max_length=400, verbose_name='物料备注', null=True)
    pcd_used = models.IntegerField(choices=PCD_USE_STATUS_CHOICES, default=0, verbose_name='明细单是否使用')

    class Meta:
        db_table = 'db_purchase_contract_detail'
        verbose_name = "合同物料明细"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pcd_num


class PurchaseContractPayDetail(models.Model):
    """合同付款协议"""
    PAY_PREPAY_CHOICES = (
        (0, '否'),
        (1, '是')
    )
    id = models.AutoField(primary_key=True)
    purchase_contract = models.ForeignKey('PurchaseContract', verbose_name='采购合同', related_name='pc_pay', on_delete=models.CASCADE)
    pay_batch = models.IntegerField(verbose_name='付款批次')
    pay_rate = models.IntegerField(verbose_name='付款比率')
    pay_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='付款金额')
    pay_planDate = models.DateField(verbose_name='计划付款日期')
    pay_prepay = models.IntegerField(choices=PAY_PREPAY_CHOICES, verbose_name='是否预付款')
    pay_remarks = models.TextField(max_length=400, verbose_name='付款备注', null=True)

    class Meta:
        db_table = 'db_purchase_contract_pay_detail'
        verbose_name = "合同付款协议"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_batch


class PurchaseOrder(models.Model):
    """采购订单"""
    PO_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    po_identify = models.CharField(max_length=15, verbose_name='采购订单编号')
    po_serial = models.CharField(max_length=4, verbose_name='采购订单流水号')
    organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='org_po', on_delete=models.CASCADE)
    supplier = models.ForeignKey('base.Supplier', verbose_name='供应商', related_name='supplier_po', on_delete=models.CASCADE)
    po_date = models.DateTimeField(default=datetime.datetime.now,verbose_name='采购订单生效日期')
    po_sum = models.IntegerField(verbose_name='采购订单总额')
    po_remarks = models.TextField(max_length=400, verbose_name='采购订单备注')
    purchase_contract = models.ForeignKey('PurchaseContract', verbose_name='采购合同', related_name='pc_po', on_delete=models.CASCADE)
    purchase_request = models.ForeignKey('purchaseRequest.PurchaseRequest', verbose_name='请购单', related_name='pr_po', on_delete=models.Model)
    pc_identify = models.CharField(max_length=15, verbose_name='采购合同编号', null=True)
    po_status = models.IntegerField(choices=PO_STATUS_CHOICES, default=0, verbose_name='采购订单状态')
    po_creator = models.CharField(max_length=20, verbose_name='采购订单创建者名字')
    po_creator_identify = models.CharField(max_length=20, verbose_name='采购订单创建者编号')
    po_created_at= models.DateTimeField(auto_now_add=True, verbose_name='采购订单创建时间')

    class Meta:
        db_table = 'db_purchase_order'
        verbose_name = "采购订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.po_identify


class OrderDetail(models.Model):
    """采购订单明细"""
    id = models.AutoField(primary_key=True)
    purchase_order = models.ForeignKey('PurchaseOrder', verbose_name='采购订单', related_name='po_od', on_delete=models.CASCADE)
    # pr_detail = models.ForeignKey('purchaseRequest.PurchaseRequest', verbose_name='请购单物料明细', related_name='pr_od', on_delete=models.CASCADE)
    # pcd_detail = models.ForeignKey('PurchaseContractDetail', verbose_name='合同物料明细', related_name='pcd_od', on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_od', on_delete=models.CASCADE)
    od_num = models.IntegerField(verbose_name='采购数量')
    od_taxRate = models.IntegerField(default=13, verbose_name='税率')
    od_tax_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税单价')
    od_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价')
    od_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税总额')
    od_tax_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='税额')
    od_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额')
    od_pr_identify = models.CharField(max_length=15, verbose_name='请购单编号')
    od_prd_remarks = models.TextField(max_length=400, verbose_name='物料备注')

    class Meta:
        db_table = 'db_order_detail'
        verbose_name = "采购订单详情"
        verbose_name_plural = verbose_name
