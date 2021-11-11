from django.shortcuts import render
from .models import Place, Menu, RegionFestival
from django.db.models import Q
import json
import kakao_selenium


def get_place_detail(request, place_name):
    place = Place.objects.filter(Q(title=place_name))
    return render(request, 'place.html', {'place': place})


def get_regionFestival_detail(request, place_name):
    RegionFestival = RegionFestival.objects.filter(Q(title=place_name))
    return render(request, 'regionfestival.html', {'RegionFestival': RegionFestival})


def set_place_data(id, region, place_type, region_money):
    kakao = kakao_selenium.kakaoCrawler()
    data = kakao.place_detail_crawl(id)
    db, created = Place.objects.update_or_create(
        kakao_place_id=data['kakao_place_id'])
    db.region = region
    db.place_type = place_type
    db.region_money = region_money

    # crawl data input
    db.title = data['title']
    db.category = data['category']
    db.location = data['location']
    db.businessHours = data['businessHours']
    for menu in data['menu']:
        m, created = Menu.objects.get_or_create(name=menu['name'])
        m.price = menu['price']
        db.menu.add(m)
    db.menu = data['menu']
    db.save()
