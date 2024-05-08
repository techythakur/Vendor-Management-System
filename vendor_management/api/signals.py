from django.db.models.signals import post_save
from .params import DAYS_OF_DELIVERY
from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models import Avg
from datetime import datetime, timedelta
from django.dispatch import receiver
from .models import HistoricalPerformance, PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save(sender, instance, *args, **kwargs):
    '''
        This signal Writes Historical Performances of Vendors
        
        NOTE: I have assumed delivery should be done under 7 days, 
        to calculate on_time_delivery_rate As there was no specific details was provided regarding delivery
    '''
    if instance:
        vendor = instance.vendor
        completed_pos = vendor.purchase_orders.filter(status='completed')
        
        completed_pos_on_time = completed_pos.filter(delivery_date__lte=F('order_date') + timedelta(days=DAYS_OF_DELIVERY)).count()
        on_time_delivery_rate = completed_pos_on_time / completed_pos.count() if completed_pos.count() > 0 else 0
        on_time_delivery_rate = on_time_delivery_rate if on_time_delivery_rate else 0
        
        quality_rating_avg = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
        quality_rating_avg = quality_rating_avg or 0
        
        completed_pos_with_response_time = completed_pos.annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
        )
        avg_response_time = completed_pos_with_response_time.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
        average_response_time = avg_response_time or 0
        
        successful_fulfilled_pos = completed_pos.exclude(issue_date__isnull=False).count()
        fulfilment_rate = successful_fulfilled_pos / vendor.purchase_orders.count() if vendor.purchase_orders.count() > 0 else 0
        fulfillment_rate = fulfilment_rate or 0
        
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.average_response_time = average_response_time
        vendor.quality_rating_avg = quality_rating_avg
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()
        
        historical_performance, _ = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=datetime.now().date())
        historical_performance.on_time_delivery_rate = on_time_delivery_rate
        historical_performance.average_response_time = average_response_time
        historical_performance.quality_rating_avg = quality_rating_avg
        historical_performance.fulfillment_rate = fulfillment_rate
        historical_performance.save()
