from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_details = serializers.CharField()
    address = serializers.CharField()
    vendor_code = serializers.CharField(max_length=50)
    on_time_delivery_rate = serializers.FloatField(default=0.0)
    quality_rating_avg = serializers.FloatField(default=0.0)
    average_response_time = serializers.FloatField(default=0.0)
    fulfillment_rate = serializers.FloatField(default=0.0)
    
class PurchaseOrderReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    vendor_id = serializers.IntegerField()
    po_number = serializers.CharField(max_length=255)
    order_date = serializers.DateTimeField()
    delivery_date = serializers.DateTimeField()
    items = serializers.JSONField()
    quantity = serializers.IntegerField()
    status = serializers.ChoiceField(choices=PurchaseOrder.STATUS_CHOICES)
    quality_rating = serializers.FloatField(allow_null=True, required=False)
    issue_date = serializers.DateTimeField()
    acknowledgment_date = serializers.DateTimeField(allow_null=True, required=False)

class HistoricalPerformanceReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    vendor_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    on_time_delivery_rate = serializers.FloatField()
    quality_rating_avg = serializers.FloatField()
    average_response_time = serializers.FloatField()
    fulfillment_rate = serializers.FloatField()


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'