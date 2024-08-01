from rest_framework import serializers as srls
from GisMeteoImage.models import ResponseGismeteoModel


class ResponseGismeteoSerializer(srls.ModelSerializer):
    image = srls.ImageField(source="image_field",
                            read_only=True,
                            required=False)

    class Meta:
        model = ResponseGismeteoModel
        fields = ("raw_data", "image", "city")
        extra_kwargs={"raw_data": {"required": False},
                      "city": {"read_only": True}}
        # write_only_fields = ("raw",)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if data["raw"] == False:
    #         data.pop("raw_data")
    #     data.pop("raw")
    #     return data
    
    async def acreate(self, validated_data, user):
        metaModel = self.Meta.model
        # user = self.context["request"].user
        return await metaModel.objects.acreate(
            raw_data=validated_data["raw_data"], user=user)
    
    async def asave(self, **kwargs):
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
        ) 


        if self.instance is not None:
            raise TypeError("Update method is invalid")
        
        self.instance = await self.acreate(self.validated_data, **kwargs)

        return self.instance

    def create(self, validated_data):
        pass

    def update(self, *args):
        pass