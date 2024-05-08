from rest_framework import viewsets
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.decorators import action
from datetime import datetime
from .params import DATE_TIME_FORMAT
from rest_framework.permissions import IsAuthenticated
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorReadSerializer, PurchaseOrderReadSerializer

class VendorViewSet(viewsets.ModelViewSet):
    '''
        Manipulates Detail of Vendors
    '''
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VendorReadSerializer
        return VendorSerializer
    
    @action(
        methods=["GET"],
        detail=False,
        url_name="performance",
        url_path="performance",
        permission_classes = [IsAuthenticated,]
    )
    def historical_performance(self, request, *args, **kwargs):
        '''
            Provides Historical Performances of Vendors
        '''
        context = {
            "msg": "",
            "flag": False
        }
        data = {}
        pk = kwargs.get('pk', None)
        try:
            vendor = Vendor.objects.get(pk=int(pk))
        except Exception:
            context["msg"] = "Error with vendor_id, Not Found!"
            return Response(context, status=HTTP_404_NOT_FOUND)
        if vendor:
            data["quality_rating_avg"] = vendor.quality_rating_avg
            data["average_response_time"] = vendor.average_response_time
            data["fulfillment_rate"] = vendor.fulfillment_rate
            data["on_time_delivery_rate"] = vendor.on_time_delivery_rate
            datewise={}
            historicalperformances = HistoricalPerformance.objects.filter(vendor=vendor)
            if historicalperformances.exists():
                for performance in historicalperformances:
                    datewise[performance.date] = {
                        "quality_rating_avg": performance.quality_rating_avg,
                        "average_response_time": performance.average_response_time,
                        "fulfillment_rate": performance.fulfillment_rate,
                        "on_time_delivery_rate": performance.on_time_delivery_rate
                    }
            data["historical_performances"] = datewise
            context["data"] = data
            context["flag"] = True
            return Response(context, status=HTTP_200_OK)
        context["msg"]="Please provide correct Vendor Id!"
        return Response(context, status=HTTP_404_NOT_FOUND)
    

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    '''
        Manipulates Data of Purchase Orders
    '''
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PurchaseOrderReadSerializer
        return PurchaseOrderSerializer
    
    @action(
        methods=["POST"],
        detail=True,
        url_name="acknowledge",
        url_path="acknowledge",
        permission_classes = [IsAuthenticated,]
    )
    def acknowledge_purchase_orders(self, request, *args, **kwargs):
        '''
            Updates Acknowldge Date of Purchase Orders
        '''
        context = {
            "msg": "",
            "flag": False
        }
        pk = kwargs.get('pk', None)
        try:
            purchase_order = PurchaseOrder.objects.get(pk=int(pk))
        except Exception:
            context["msg"] = "Error with Purchase Order id, Not Found!"
            return Response(context, status=HTTP_404_NOT_FOUND)
        acknowledge_date = self.request.POST.get("acknowledge_date", None)
        if acknowledge_date:
            acknowledge_date = datetime.strptime(acknowledge_date, DATE_TIME_FORMAT)
            purchase_order.acknowledgment_date = acknowledge_date
            purchase_order.save()
            context["msg"] = "Acknowledge Date saved Successfully!"
            context["flag"] = True
            return Response(context, status=HTTP_200_OK)
        context["msg"]="Please provide Acknowledge Date!"
        return Response(context, status=HTTP_404_NOT_FOUND)