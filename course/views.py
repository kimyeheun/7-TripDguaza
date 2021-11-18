from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CourseForm, CourseItemForm
from .models import Course, CourseItem
from main.models import User

def course_create(request):
    """
    코스 생성
    """
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        request.POST._mutable = True
        request.POST['user'] = request.user
        if form.is_valid():
            form.save()
        else:
            validation = 'error'
            return render(request, 'course_create.html', {'validation': validation})
        return HttpResponseRedirect('../courseitem_create')
    form = CourseForm(request.FILES)
    return render(request, 'course_create.html', {'form': form})


def courseitem_create(request):
    """
    코스 아이템 생성
    """
    if request.method == 'POST':
        form = CourseItemForm(request.POST, request.FILES)
        request.POST._mutable = True
        request.POST['user'] = request.user
        if form.is_valid():
            form.save()
        else:
            validation = 'error'
            return render(request, 'courseitem_create.html', {'validation': validation})
        return HttpResponseRedirect('../course_list')
    form = CourseItemForm(request.FILES)

    return render(request, 'courseitem_create.html', {'form': form})


def course_list(request):
    """
    코스 조회
    생성 날짜 순으로 리스트를 보여줌
    로그인하지 않은 유저가 히스토리 접근할 경우 로그인 페이지로 리다이렉트함
    """
    if request.method == 'POST':

        return HttpResponseRedirect('../course_detail')
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin/')
    courses = Course.objects.all().order_by('created_at')
    context = {
        'courses': courses,
    }
    return render(request, 'course_list.html', context)


def course_detail(request, id):
    """
    코스 자세히보기
    pk 값을 기준으로 페이지를 보여줌
    """
    courseitems = CourseItem.objects.filter(course=id)
    context = {
        'courseitems': courseitems,
    }
    return render(request, 'course_detail.html', context)


def course_delete(request, id):
    """
    코스 삭제
    해당하는 id의 Course item 삭제
    """
    item = get_object_or_404(Course, pk=id)
    if request.method == 'POST':
        item.delete()
        return redirect('course_list')


# def course_update(request):
#     """
#     코스 수정
#     해당하는 id의 코스 수정
#     글 수정 시, 기존의 내용 폼에 유지
#     """
#     if request.method == 'POST' and 'id' in request.POST:
#         item = get_object_or_404(Course, pk=request.POST.get('id'))
#         form = CourseUpdateForm(request.POST, request.FILES, instance=item)
#         if form.is_valid():
#             form.save()
#         else:
#             validation = 'error'
#             return render(request, 'course_update.html', {'validation': validation})
#     elif 'id' in request.GET:
#         item = get_object_or_404(Course, pk=request.GET.get('id'))
#         form = CourseForm(instance=item)
#         return render(request, 'course_update.html', {'form': form})
#     return HttpResponseRedirect("../course_list")



