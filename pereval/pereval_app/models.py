from django.db import models

'''
{
    "beauty_title": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "", // что
соединяет, текстовое
поле
"add_time": "2021-09-22 13:18:13",
"user": {"email": "qwerty@mail.ru",
         "fam": "Пупкин",
         "name": "Василий",
         "otc": "Иванович",
         "phone": "+7 555 55 55"},
"coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"}
level: {"winter": "", // Категория трудности.В
разное время года перевал может
иметь разную категорию трудности
"summer": "1А",
"autumn": "1А",
"spring": ""},
images: [{data: "<картинка1>", title: "Седловина"}, {data: "<картинка>", title: "Подъём"}]
}
'''

'''
Пользователи которые передают информацию
'''
class Turist(models.Model):
    fam = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    otc = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    phone = models.IntegerField(unique=True, verbose_name='Телефон')
    email = models.CharField(max_length=100, unique=True, verbose_name='почта')
    def __str__(self):
        return f'{self.fam} {self.name} {self.otc}'

'''
Информаци я о местоположении и высоте
'''
class Coordinats(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')
    def __str__(self):
        return f"широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}"

'''
Время года. В зависимости от времени года меняется и сложность
'''
class HardLevel(models.Model):
    winter = models.CharField(max_length=6, null=True, blank=True, verbose_name='Зима')

    summer = models.CharField(max_length=6, null=True, blank=True, verbose_name='Лето')

    autumn = models.CharField(max_length=6, null=True, blank=True, verbose_name='Осень')

    spring = models.CharField(max_length=6, null=True, blank=True, verbose_name='Весна')

    def __str__(self):
        return f"зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}"

'''
Внесение информации о перевале
'''
class Mounts(models.Model):

    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название')
    beautyTitle = models.CharField(max_length=255, default='пер.',verbose_name='Краткое название')
    other_titles = models.CharField(max_length=255, blank=True, null=True, verbose_name='Другое название')
    connect = models.CharField(max_length=255, blank=True, null=True, verbose_name='К чему относится')
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Turist, on_delete=models.CASCADE, default=None, verbose_name='Турист')
    coord = models.OneToOneField(Coordinats, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Координаты')
    status = models.CharField(max_length=2, verbose_name='Статус')
    level = models.ForeignKey(HardLevel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Уровень сложности')

    def __str__(self):
        return f'{self.pk} {self.beautyTitle}'

def get_path_upload_images(instance, file):
    return f'images/mount-{instance.mount.id}/{file}'

'''
Изображения
'''
class Images(models.Model):
    mount = models.ForeignKey(Mounts, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to=get_path_upload_images, blank=True, null=True, verbose_name='Изображение')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название')

    def __str__(self):
        return f'{self.mount}'
