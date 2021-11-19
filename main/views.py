from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignInForm, UpdateUserInfoForm, SignUpForm
from .models import User
from django.contrib.auth import login, authenticate, logout


def main(request):
    return render(request, "main.html")


def signup(request):
    """
    회원가입
    회원가입 폼 양식이 유효하면 회원가입 완료 후 로그인 페이지로 이동
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect('../userinfo/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../signin/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    """
    로그인
    로그인 폼 양식이 유효하면, 로그인 인증 과정을 거치고 인증이 완료되면 메인 페이지로 돌아감
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect('../userinfo')
    args = {}
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.data['email'], password=form.data['password'])
            login(request, user)
            return HttpResponseRedirect('../userinfo')
    else:
        form = SignInForm()
    args['form'] = form
    return render(request, 'signin.html', args)


def signout(request):
    """
    로그아웃 한 뒤 메인페이지로 이동함
    """
    logout(request)
    return HttpResponseRedirect('../')


def userinfo(request):
    """
    내 정보 조회(마이페이지)
    현재 로그인 되어있는 사용자의 정보를 사용자의 pk값으로 렌더링해서 보여줌
    """
    if request.user.is_authenticated:
        user_id = request.user.id
        context = {
            'users': User.objects.filter(id=user_id)
        }
        return render(request, 'userinfo.html', context)
    else:
        return HttpResponseRedirect('../signin')


@login_required
def userinfo_update(request):
    """
    회원 정보 수정
    회원 정보 수정 폼 양식이 유효하다면, 변경사항을 저장하고 변경된 회원정보를 다시 보여줌
    """
    if request.method == 'POST':
        form = UpdateUserInfoForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            # messages.error(request, '형식에 맞게 작성해주세요(YYYY-MM-DD)')
            return HttpResponseRedirect('userinfo_update')
    else:
        form = UpdateUserInfoForm(instance=request.user)
        return render(request, 'userinfo_update.html', {'form': form})
    return HttpResponseRedirect("../userinfo/")
