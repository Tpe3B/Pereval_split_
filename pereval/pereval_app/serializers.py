from drf_writable_nested import WritableNestedModelSerializer
from .models import *
from rest_framework import serializers


class TuristSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turist
        fields = [
            'email',
            'fam',
            'name',
            'otc',
            'phone',
        ]
        verbose_name = 'Турист'

    def save(self, **kwargs):
        self.is_valid()
        user = Turist.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = Turist.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
            return new_user


class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height'
        ]
        verbose_name = 'Координаты'


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring'
        ]
        verbose_name = 'Уровень сложности'


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.URLField()

    class Meta:
        model = Images
        fields = [
            'image',
            'title',
        ]
        verbose_name = 'Фото'





class MountsSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = TuristSerializer()
    coord = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = Mounts
        fields = [
            'id',
            'beautyTitle',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'user',
            'coord',
            'level',
            'images',
            'status',
        ]
        read_only_fields = ['status']

    def validate(self, value):

        user_data = value['user']

        if self.instance:
            if (user_data['email'] != self.instance.user.email or
                    user_data['fam'] != self.instance.user.fam or
                    user_data['name'] != self.instance.user.name or
                    user_data['otc'] != self.instance.user.otc or
                    user_data['phone'] != self.instance.user.phone):
                raise serializers.ValidationError()

        return value