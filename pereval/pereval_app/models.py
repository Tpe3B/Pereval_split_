from django.db import models
from django.utils.translation import gettext_lazy as _

'''Пользователи которые передают информацию'''
class Turist(models.Model):
    email = models.CharField(max_length=100, unique=True, verbose_name='почта')
    fam = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    otc = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    phone = models.IntegerField(unique=True, verbose_name='Телефон')

    def __str__(self):
        return f'{self.fam} {self.name} {self.otc}'

'''Информаци я о местоположении и высоте'''
class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')
    def __str__(self):
        return f"широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}"


'''Время года. В зависимости от времени года меняется и сложность'''
class Level(models.Model):
    class LevelChoice(models.TextChoices):
        '''Класс уровня'''
        LEVEL1 = "1a", _("1А")
        LEVEL2 = "1b", _("1Б")
        LEVEL3 = "2a", _("2А")
        LEVEL4 = "2b", _("2Б")
        LEVEL5 = "3a", _("3А")
        LEVEL6 = "3b", _("3Б")

    winter = models.CharField(max_length=6, choices=LevelChoice.choices, default=LevelChoice.LEVEL1, null=True, blank=True, verbose_name='Зима')
    summer = models.CharField(max_length=6, choices=LevelChoice.choices, default=LevelChoice.LEVEL1, null=True, blank=True, verbose_name='Лето')
    autumn = models.CharField(max_length=6, choices=LevelChoice.choices, default=LevelChoice.LEVEL1, null=True, blank=True, verbose_name='Осень')
    spring = models.CharField(max_length=6, choices=LevelChoice.choices, default=LevelChoice.LEVEL1, null=True, blank=True, verbose_name='Весна')
    def __str__(self):
        return f"зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}"

'''Внесение информации о перевале'''
class Mounts(models.Model):
    '''Класс статуса'''
    class Status(models.TextChoices):
        NEW = "NW", _("Новый")
        PENDING = "PN", _("В работе")
        ACCEPTED = "AC", _("Принято")
        REJECTED = "RJ", _("Не принято")


    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название')
    beautyTitle = models.CharField(max_length=255, default='пер.', verbose_name='Краткое название')
    other_titles = models.CharField(max_length=255, blank=True, null=True, verbose_name='Другое название')
    connect = models.CharField(max_length=255, blank=True, null=True, verbose_name='К чему относится')
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Turist, on_delete=models.CASCADE, default=None, verbose_name='Турист')
    coord = models.OneToOneField(Coords, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Координаты')
    status = models.CharField(max_length=2, choices=Status.choices, default="NW", verbose_name='Статус')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Уровень сложности')

    def __str__(self):
        return f'{self.pk} {self.beautyTitle}'
def get_path_upload_images(instance, file):
    return f'images/mount-{instance.mount.id}/{file}'


'''Изображения'''
class Images(models.Model):
    mount = models.ForeignKey(Mounts, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to=get_path_upload_images, blank=True, null=True, verbose_name='Изображение')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название')
    def __str__(self):
        return f'{self.mount}'
