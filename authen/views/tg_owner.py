from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from authen.models import TGOwner
from authen.serializers.tg_basic import TGOwnerModelSerializer
from authen.backend.permissions import TGIsAdminOrOwner


class OwnerViewSet(ModelViewSet):
    queryset = TGOwner.objects.prefetch_related(TGOwner.TGUSER_RELATE_FIELD)
    serializer_class = TGOwnerModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "update" or self.action == "retrieve":
            permission_classes = (*permission_classes, TGIsAdminOrOwner)
        elif self.action == "create":
            permission_classes = ()
        return [permission() for permission in permission_classes]
