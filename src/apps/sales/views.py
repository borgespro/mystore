from rest_framework import generics, permissions

from apps.core.models import User
from .models import SaleOrder
from .serializers import SaleOrderSerializer


class SaleOrderView(generics.ListCreateAPIView):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        queryset = super(SaleOrderView, self).get_queryset()
        if user.user_type == User.CUSTOMER:
            return queryset.filter(customer=user)
        else:
            return queryset
