from rest_framework import serializers as serialz
from authen.models import TGUser, TGOwner


class TGUserModelSerializer(serialz.ModelSerializer):
    class Meta:
        model = TGUser
        fields = ["user_id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return TGUser.objects.create_user(**validated_data)
    

class TGOwnerModelSerializer(serialz.ModelSerializer):
    tg_user = TGUserModelSerializer(read_only=True)

    user_id = serialz.PrimaryKeyRelatedField(
        queryset=TGUser.objects.all(), source="tg_user", write_only=True
    )

    class Meta:
        model = TGOwner
        fields = ("tg_user", "user_id", "first_name", "last_name")
