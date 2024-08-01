from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from asgiref.sync import async_to_sync

from GisMeteoImage.models import ResponseGismeteoModel
from GisMeteoImage.serializers import ResponseGismeteoSerializer


# class GetGismeteoImageView(APIView):
#     # permission
#     # authenthicate
    
#     async def get(self, request): # how to async this?
#         resp = await ResponseGismeteoModel.objects.find_around_time(
#             city=request.user.owner.city,
#             now_time=now()
#             )
        
#         if resp:
#             serializer = ResponseGismeteoSerializer(data={"raw_data": resp.raw_data})
#         else:
#             serializer = ResponseGismeteoSerializer(data={})
#         if serializer.is_valid(): #else
#             await serializer.asave(user=request.user)

#         return Response(serializer.data)

class GismeteoImageViewSet(GenericViewSet):
    serializer_class = ResponseGismeteoSerializer


    @action(methods=["GET"], detail=False, url_path=r"now")
    def weather_now(self, request): # how to async this?
        resp = ResponseGismeteoModel.objects.find_around_time(
            city=request.user.owner.city,
            now_time=now()
            )
        
        if resp:
            serializer = self.get_serializer(data={"raw_data": resp.raw_data})
        else:
            serializer = self.get_serializer(data={"raw_data": None})
        if serializer.is_valid(): #else
            async_to_sync(serializer.asave)(user=request.user)

        return Response(serializer.data)
        


