from rest_framework import serializers as srlz

from authen.serializers.user_create import TGUserModelSerializer
from authen.models import TGUser, TGOwner
    

class TGOwnerCreateModelSerializer(srlz.ModelSerializer):
    user_id = srlz.IntegerField(source="tg_user.user_id")
    username = srlz.CharField(source="tg_user.username")

    class Meta:
        model = TGOwner
        fields = ("username", "user_id", "first_name", "last_name")

    def create(self, validated_data):
        tg_user = TGUserModelSerializer(data=validated_data.pop("tg_user"))
        tg_user.is_valid(raise_exception=True)
        user = tg_user.save()
        return self.Meta.model.objects.create_owner(user=user,
                                                    **validated_data)
