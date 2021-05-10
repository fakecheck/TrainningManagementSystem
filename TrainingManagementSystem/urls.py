# coding=utf-8
"""TMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from.views import *

urlpatterns = [
    # 注册 path 'register'
    # 管理员注册 / 修改个人信息
    path('register/admin', AdminRegisterAPI.as_view()),
    # 讲师注册 / 修改个人信息
    path('register/teacher', TeacherRegisterAPI.as_view()),
    # 学员注册 / 修改个人信息
    path('register/student', StudentRegisterAPI.as_view()),

    # 登录 path 'login'
    # 管理员登录
    path('login/admin', AdminLoginAPI.as_view()),
    # 讲师登录
    path('login/teacher', TeacherLoginAPI.as_view()),
    # 学员登录
    path('login/student', StudentLoginAPI.as_view()),

    # 管理员
    # 培养方案相关
    # 培养方案管理
    path('admin/plan', AdminPlanManagement.as_view()),
    # 默认培养方案设置
    path('admin/plan/default', AdminPlanSetting.as_view()),
    # 学员培养方案设置
    path('admin/plan/set', AdminPlanAppoint.as_view()),

    # 考核方案管理
    path('admin/requirement', AdminRequirementManagement.as_view()),
    # 默认考核方案设置
    path('admin/requirement/default', AdminRequirementSetting.as_view()),
    # 学员考核方案设置
    path('admin/requirement/set', AdminRequirementAppoint.as_view()),


    # 管理员
    # 培训课程相关
    path('admin/course', AdminCourseManagement.as_view()),
    #
    # # 讲师
    # # 讲师-发起签到
    # path('teacher/checkin', TeacherCheckIn.as_view()),
    # 成绩评定&结课
    path('teacher/grading', TeacherGrading.as_view()),

    # 学生
    # 获取课程列表
    path('courseList', StudentCourseList.as_view()),
    # # 完成签到
    # path('student/checkin', StudentCheckIn.as_view()),
    # # 评价课程
    path('student/comment', StudentComment.as_view()),
    #
    # 课程讨论区
    # Issue
    path('disscuss/issue', CourseIssue.as_view()),
    # discussion
    path('disscuss/issue/discussion', CourseDiscussion.as_view()),
    #
    # # 课程管理
    # # 文件管理
    # # TODO
    # # 组队管理
    # path('course/grouplist', CourseGroupManagement.as_view()),
    # path('course/group', CourseGroupManagement.as_view()),
    # path('course/group-rdmset', CourseGroupRandomSet.as_view()),
    # # 队伍文件管理
    # # TODO
]
