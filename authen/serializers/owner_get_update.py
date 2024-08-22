from rest_framework import serializers as srlz

from authen.models import TGUser, TGOwner
from authen.serializers.user_get_update import TGUserRetrieveUpdateModelSerializer
from authen.bases.models import LANGUAGE_CHOICE


class TGOwnerRetrieveUpdateModelSerializer(srlz.ModelSerializer):
    user_id = srlz.IntegerField(source="tg_user.user_id", read_only=True)
    username = srlz.CharField(source="tg_user.username", read_only=True)
    language = srlz.ChoiceField(choices=LANGUAGE_CHOICE, source="tg_user.language")
    
    class Meta:
        model = TGOwner
        fields = ("user_id", "username", "first_name", "last_name",
                  "language", "city", "lat", "lon") #city validate
        extra_kwargs = {
            "lat": {"read_only": True}, 
            "lon": {"read_only": True}
            }
    
    def update(self, instance, validated_data):
        user_ser = TGUserRetrieveUpdateModelSerializer(instance.tg_user, validated_data.pop("tg_user"))
        user_ser.is_valid(raise_exception=True)
        user_ser.save()
        return super().update(instance=instance, validated_data=validated_data)

