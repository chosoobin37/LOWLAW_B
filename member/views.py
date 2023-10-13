from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import admin
from social_django.views import complete
from django.db import IntegrityError

from django.urls import reverse
from .forms import NewProfileChangeForm
from allauth.socialaccount.helpers import render_authentication_error

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import JsonResponse

admin.site.register(Token)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError as e:
            messages.error(request, '이미 등록된 이메일입니다.')
            return redirect('register')
        else:
            messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_redirect')  # 로그인 성공 시 'home' 주소로 이동
        else:
            messages.error(request, '이메일과 비밀번호가 일치하지 않습니다.')  # 에러 메시지 출력
            return redirect('login')  # 로그인 실패 시 다시 로그인 페이지로 이동
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_admin(request):
    if not request.user.is_superuser:
        return redirect('home')
    users = User.objects.all()
    return render(request, 'user_admin.html', {'users': users})

@login_required
def mypage(request):
    user = request.user

    if request.method == 'POST':
        profile_form = NewProfileChangeForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '사용자 정보가 수정되었습니다.')
    else:
        profile_form = NewProfileChangeForm(instance=user)
    
    return render(request, 'mypage.html', {'user': user, 'profile_form': profile_form})

@login_required
def user_delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, '회원 탈퇴가 완료되었습니다.')
        return render(request, 'user_delete.html', {'is_deleted': True})
    
    return render(request, 'user_delete.html', {'is_deleted': False})

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


