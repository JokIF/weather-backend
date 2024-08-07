from rest_framework import serializers as serialz
from authen.models import TGUser, TGOwner


class TGUserModelSerializer(serialz.ModelSerializer):
    class Meta:
        model = TGUser
        fields = ["user_id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True, "default": None}}

    def create(self, validated_data):
        return TGUser.objects.create_user(**validated_data)
    

class TGOwnerModelSerializer(serialz.ModelSerializer):
    user_id = serialz.IntegerField(source="tg_user.user_id")
    username = serialz.CharField(source="tg_user.username")

    class Meta:
        model = TGOwner
        fields = ("username", "user_id", "first_name", "last_name")

    def create(self, validated_data):
        tg_user = TGUserModelSerializer(data=validated_data.pop("tg_user"))
        tg_user.is_valid(raise_exception=True)
        user = tg_user.save()
        return self.Meta.model.objects.create_owner(user=user,
                                                    **validated_data)
