from rest_framework import viewsets
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, VendorReadSerializer, PurchaseOrderReadSerializer, HistoricalPerformanceReadSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VendorReadSerializer
        return VendorSerializer
    
    @action(
        methods=["GET"],
        detail=False,
        url_name="performance",
        url_path="performance",
    )
    def historical_performance(self, pk=None):
        pass
    

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PurchaseOrderReadSerializer
        return PurchaseOrderSerializer

class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HistoricalPerformanceReadSerializer
        return HistoricalPerformanceSerializer