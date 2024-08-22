from rest_framework import serializers as srlz
from authen.models import TGUser


class TGUserModelSerializer(srlz.ModelSerializer):
    class Meta:
        model = TGUser
        fields = ["user_id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True, "default": None}}

    def create(self, validated_data):
        return TGUser.objects.create_user(**validated_data)