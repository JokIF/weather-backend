from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from authen.models import TGOwner
from authen.serializers import TGOwnerCreateModelSerializer, TGOwnerRetrieveUpdateModelSerializer
from authen.backend.permissions import TGIsAdminOrOwner


class OwnerViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin, 
                   GenericViewSet):
    queryset = TGOwner.objects.prefetch_related(TGOwner.TGUSER_RELATE_FIELD)
    permission_classes = (IsAuthenticated, TGIsAdminOrOwner)

    def get_serializer_class(self):
        if self.action == "create":
            return TGOwnerCreateModelSerializer
        return TGOwnerRetrieveUpdateModelSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "create":
            permission_classes = ()
        return [permission() for permission in permission_classes]
    
    def get_object(self):
        obj = self.request.user.owner
        self.check_object_permissions(self.request, obj)
        return obj
