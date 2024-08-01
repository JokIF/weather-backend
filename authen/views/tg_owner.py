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
        if self.request.parser_context.get("kwargs"):
            permission_classes = (*permission_classes, TGIsAdminOrOwner)
        else:
            permission_classes = (*permission_classes, IsAdminUser)
        return [permission() for permission in self.permission_classes]
