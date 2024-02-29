from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import *
from .models import *


class MoUserViewSet(viewsets.ModelViewSet):
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


class MountpassViewSet(viewsets.ModelViewSet):
    queryset = Mounts.objects.all()
    serializer_class = MountsSerializer

    # Создаем перевал
    def create(self, request, *args, **kwargs):
        serializer = MountsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Успешно!',
                    'id': serializer.data['id'],
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Некорректный запрос серверу',
                    'id': None,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка сервера',
                    'id': None,
                }
            )
