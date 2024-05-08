from django.db import models

class Vendor(models.Model):
    '''
        Stores Essential information about each vendor and their performance metrics.
    '''
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

class PurchaseOrder(models.Model):
    '''
        Stores details of each purchase order and is used to calculate various performance metrics.
    '''
    PENDING="pending"
    CANCELLED="cancelled"
    COMPLETED="completed"
    STATUS_CHOICES = [
        (PENDING, "pending"),
        (CANCELLED, "cancelled"),
        (COMPLETED, "completed")
    ]
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
    po_number = models.CharField(max_length=255, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="pending")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

class HistoricalPerformance(models.Model):
    '''
        Stores historical data of vendor performance.
    '''
    vendor = models.ForeignKey(Vendor, related_name='historical_performances', on_delete=models.CASCADE)
    date = models.DateField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
