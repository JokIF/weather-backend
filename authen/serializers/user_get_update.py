from rest_framework import serializers as srlz

from authen.models import TGUser
from authen.bases.models import LANGUAGE_CHOICE


class TGUserRetrieveUpdateModelSerializer(srlz.ModelSerializer):
    language = srlz.ChoiceField(choices=LANGUAGE_CHOICE)

    class Meta:
        model = TGUser
        fields = ("user_id", "username", "language")
        extra_kwargs = {"user_id": {"read_only": True},
                        "username": {"read_only": True}}