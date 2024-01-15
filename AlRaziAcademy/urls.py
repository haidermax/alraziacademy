"""
URL configuration for AlRaziAcademy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.conf.urls.static import static
from accounts.views import  login_page,register,activate, user_profile,check_username_availability
from index.views import index,dashboard
from course.views import *
urlpatterns = [
    path('cpanel/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('login/', login_page, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('check-username/', check_username_availability, name='check_username_availability'),
    path('register/', register, name='register'),
    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', user_profile, name='profile'),
    path('dashboard/', dashboard,name='dashboard'),
    path('subject/create/', create_subject, name='create_subject'),
    path('subject/management/', subject_management, name='subject_management'),
    path('subject/details/', get_subject_details, name='get_subject_details'),
    path('subject/remove/', remove_subject, name='remove_subject'),
    path('subject/edit/<int:subject_id>/', edit_subject, name='edit_subject'),
    path('subject/members/', subject_members, name='subject_members'),
    path('remove-member/', remove_member, name='remove_member'),
    path('add-member/', add_member, name='add_member'),
    path('lecture-management/', lecture_management, name='lecture_management'),
    path('edit-lecture/<int:lecture_id>/', edit_lecture, name='edit_lecture'),
    path('remove-lecture/', remove_lecture, name='remove_lecture'),
    path('user-management/', user_management, name='user_management'),
    path('lecture_search/', lecture_search, name='lecture_search'),
    path('lecture_subject/', lecture_subject, name='lecture_subject'),
    path('search-users/', search_users, name='search_users'),
    path('subject/members/ajax/', get_members_table, name='get_members_table'),
    path('create_speciality/', create_speciality, name='create_speciality'),
    path('lectures/create/', create_lecture, name='create_lecture'),
    path('mycourses/', mycourses, name='my_courses'),
    path('lect/<int:lecture>', lecture, name='lect'),
    path('<dept>/<grade>/', grade, name='grade'),
    path('<grade>/subject/<int:subject>/', subject, name='subject'),
    path('<dept>/', dept, name='dept'),
    path('', index, name='index'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)