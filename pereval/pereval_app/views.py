import django_filters
import django_filters.rest_framework
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from .serializers import *
from .models import *
# from django.http import JsonResponse
# from rest_framework import viewsets, status, generics
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
#
# from .serializers import *


class TuristViewSet(viewsets.ModelViewSet):
    queryset = Turist.objects.all()
    serializer_class = TuristSerializer
    filterset_fields = ['fam', 'name', 'otc', 'email']
class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer
class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
class MountsViewSet(viewsets.ModelViewSet):
    queryset = Mounts.objects.all()
    serializer_class = MountsSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('user__email',)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)




    # def create(self, request, *args, **kwargs):
    #     serializer = MountsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {
    #                 'status': status.HTTP_200_OK,
    #                 'message': 'Успешно!',
    #                 'id': serializer.data['id'],
    #             }
    #         )
    #
    #     if status.HTTP_400_BAD_REQUEST:
    #         return Response(
    #             {
    #                 'status': status.HTTP_400_BAD_REQUEST,
    #                 'message': 'Некорректный запрос серверу',
    #                 'id': None,
    #             }
    #         )
    #
    #     if status.HTTP_500_INTERNAL_SERVER_ERROR:
    #         return Response(
    #             {
    #                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                 'message': 'Ошибка сервера',
    #                 'id': None,
    #             }
    #         )

    def update(self, request, *args, **kwargs):
        mount = self.get_object()
        if mount.status == 'NW':
            serializer = MountsSerializer(mount, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'state': '1',
                        'message': 'Изменения в записи внесены'
                    }
                )
            else:
                return Response(
                    {
                        'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    'state': '0',
                    'message': f'Текущий статус: {mount.get_status_display()}, изменить запись нельзя!'
                }
            )