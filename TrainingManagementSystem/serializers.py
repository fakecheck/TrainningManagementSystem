# coding=utf-8
from rest_framework import serializers
from .models import *


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlans
        fields = '__all__'


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'


class CourseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInfo
        exclude = ('checkInTimes', 'modifyTime', 'createTime')


class PlanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDetail
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'
