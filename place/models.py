from django.db import models

PLACE_CHOICES = (
    (0, '식당'),
    (1, '관광지')
)
REGION_MONEY_AVALIABLE = (
    (0, '불가능'),
    (1, '가능')
)


class Menu(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Place(models.Model):
    kakao_place_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    category = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    businessHours = models.CharField(max_length=100, blank=True)
    menu = models.ManyToManyField(
        Menu, related_name='menu', blank=True)
    place_type = models.IntegerField(choices=PLACE_CHOICES, null=True)
    region_money = models.IntegerField(
        choices=REGION_MONEY_AVALIABLE, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.region + " " + self.title


class RegionFestival(models.Model):
    title = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    description = models.CharField(max_length=500, blank=True)
    period = models.CharField(max_length=20)
    host_info = models.CharField(max_length=20)

    def __str__(self):
        return self.title
