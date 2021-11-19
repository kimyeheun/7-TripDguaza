from django.shortcuts import render, redirect, get_object_or_404
from .models import Place, Menu, RegionFestival
from django.db.models import Q
import json
from .kakao_selenium import kakaoCrawler
import csv


def test(request):
    return render(request, "test.html")


def region_detail(request, region_name):
    place_list = Place.objects.filter(region=region_name)
    return render(request, 'region_detail.html', {'region_name': region_name, 'place_list': place_list})


def get_place_detail(request, kakao_place_id):
    place = get_object_or_404(Place, kakao_place_id=kakao_place_id)
    return render(request, 'get_place_detail.html', {'place': place})


def set_place_detail(request):
    new_place = Place()
    new_place.kakao_place_id = request.POST['kakao_place_id']
    new_place.region = request.POST['region']
    new_place.place_type = request.POST['place_type']
    new_place.region_money = request.POST['region_money']
    new_place.save()
    kakao_crawl(request.POST['kakao_place_id'])
    return redirect('get_place_detail', new_place.kakao_place_id)


def get_regionFestival_detail(request, kakao_place_id):
    RegionFestival = get_object_or_404(
        RegionFestival, kakao_place_id=kakao_place_id)
    return render(request, 'regionfestival.html', {'RegionFestival': RegionFestival})


def kakao_crawl(id):
    kakao = kakaoCrawler()
    data = kakao.place_detail_crawl(id)
    db, created = Place.objects.update_or_create(
        kakao_place_id=data['kakao_place_id'])
    # crawl data input
    db.title = data['title']
    db.category = data['category']
    db.location = data['location']
    db.businessHours = data['businessHours']
    for menu in data['menu']:
        m, created = Menu.objects.get_or_create(
            name=menu['name'], price=menu['price'])
        db.menu.add(m)
    db.save()


# 지역축제 데이터 업로드
def csv_to_db():
    csv_path = "./place/region_festival_busan.csv"
    with open(csv_path, newline='') as csvfile:
        fieldnames = ['region', 'title', 'period', 'description', 'host_info']
        data = csv.DictReader(csvfile)

        for row in data:
            RegionFestival.objects.create(
                region=row['region'],
                title=row['title'],
                period=row['period'],
                description=row['description'],
                host_info=row['host_info']
            )
