from django.urls import include, path
from member import views
from django.contrib import admin
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount import views as socialaccount_views

#mypage
from member.views import mypage

urlpatterns = [
    # 빈 경로에 대한 URL 패턴 추가
    path('', views.home, name='home'),

    # 회원가입 기능
    path('register/', views.register, name='register'),

    # 회원 관리자 페이지
    path('user_admin/', views.user_admin, name='user_admin'),

    # 로그인 기능
    path('login/', views.user_login, name='login'),

    # 로그아웃 기능
    path('logout/', views.user_logout, name='logout'),

    # # 소셜 로그인 기능
    # # path('accounts/kakao/login/callback/', views.social_login, name='social_login'),
    # path('accounts/', include('allauth.urls')),

    # 관리자 페이지
    path('admin/', admin.site.urls),

    #마이페이지
    path('mypage/', mypage, name='mypage'),

    #회원탈퇴
    path('user-delete/', views.user_delete, name='user_delete'),

    # #구글로그인
    # path('welcome/', views.welcome, name='welcome'),

]

# 로그인 성공 시 홈 화면으로 리다이렉트하는 URL 패턴 추가
urlpatterns += [
    path('home/', views.home, name='home_redirect'),
]
