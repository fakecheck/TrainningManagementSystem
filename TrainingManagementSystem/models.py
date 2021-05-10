# coding=utf-8
from django.db import models


class CourseStatus(models.IntegerChoices):
    NOT_AVAILABLE = 0  # 不可用，未知状态
    DELETED = 1  # 课程已删除
    OPEN = 2  # 课程正开放
    CLOSED = 3  # 课程已关闭
    SETTLED = 4  # 课程已结课


class IssueStatus(models.IntegerChoices):
    CLOSED = 1  # 问题已解决/已关闭
    OPEN = 2  # 开放问题


class GradeType(models.IntegerChoices):
    CARDINAL = 0  # 基数制
    HUNDREDMARK = 1  # 百分制
    HUNDREDMARKFLOAT = 2  # 百分制支持浮点


class Gender(models.IntegerChoices):
    MALE = 1  # 男性
    FEMALE = 2  # 女性


class CourseRating(models.IntegerChoices):
    ONESTAR = 1
    TWOSTAR = 2
    THREESTAR = 3
    FOURSTAR = 4
    FIVESTAR = 5


class CourseInfo(models.Model):
    # 课程名称
    courseName = models.CharField(max_length=30)
    # 课程描述
    courseDescription = models.TextField(max_length=200, null=True)
    # 课程时间
    courseTime = models.CharField(max_length=20, null=True)
    # 课程地点
    courseLocation = models.CharField(max_length=40, null=True)
    # 学分奖励
    creditAward = models.IntegerField(null=True)
    # 课程状态
    courseStatus = models.IntegerField(choices=CourseStatus.choices, default=CourseStatus.NOT_AVAILABLE)

    # 讲师名称
    teacherName = models.CharField(max_length=10)
    # 讲师描述
    teacherDescription = models.TextField(max_length=200, null=True)
    # 讲师ID
    teacherID = models.IntegerField()

    # 开放时间
    openFrom = models.DateTimeField(null=True)
    # 开放截止
    openUntil = models.DateTimeField(null=True)

    # 额外存储信息
    extra = models.TextField(max_length=500)

    # 创建时间
    createTime = models.DateTimeField(auto_now_add=True)
    # 修改时间
    modifyTime = models.DateTimeField(auto_now=True)


class TrainingPlans(models.Model):
    # 方案名称
    planName = models.CharField(max_length=30)
    # 方案说明
    description = models.TextField(null=True, max_length=300)
    # 创建时间
    createTime = models.DateTimeField(auto_now_add=True)
    # 修改时间
    modifyTime = models.DateTimeField(auto_now=True)


class PlanDetail(models.Model):
    # 课程ID
    courseID = models.IntegerField()
    # 方案ID
    planID = models.IntegerField()


class CourseTaking(models.Model):
    # 学生ID
    studentID = models.IntegerField()
    # 课程ID
    courseID = models.IntegerField()
    # 课程是否结算
    settled = models.BooleanField(default=False)
    # 学分奖励
    creditAward = models.IntegerField(null=True)
    # 有效时间
    validFrom = models.DateTimeField(null=True)
    # 失效时间
    validUntil = models.DateTimeField(null=True)
    # 成绩(百分制/基数制)
    grade = models.FloatField(null=True)
    # 成绩类型
    gradeType = models.IntegerField(choices=GradeType.choices, null=True)

    # 额外存储信息
    extra = models.TextField(max_length=500)


class CourseGrouping(models.Model):
    # 课程ID
    courseID = models.IntegerField()
    # 小组ID
    groupID = models.IntegerField()
    # 小组名称
    groupName = models.CharField(max_length=30)
    # 小组人数
    groupCounts = models.IntegerField()
    # 小组最大人数
    groupLimits = models.IntegerField()


class CourseComments(models.Model):
    # 课程ID
    courseID = models.IntegerField()
    # 学生ID
    studentID = models.IntegerField()
    # 内容
    content = models.TextField(max_length=300)
    # 打分
    rate = models.IntegerField(choices=CourseRating.choices)
    # 创建时间
    createTime = models.DateTimeField(auto_now_add=True)


class Requirement(models.Model):
    # 考核方案名称
    planName = models.CharField(max_length=30)
    # 考核方案学分要求
    requirement = models.IntegerField()
    # 考核方案截止时间
    deadline = models.DateTimeField()


class Teacher(models.Model):
    # 工号
    workID = models.IntegerField(unique=True)
    # 姓名
    name = models.CharField(max_length=10)
    # 性别
    gender = models.IntegerField(choices=Gender.choices, null=True, default=None)
    # 手机号
    phoneNumber = models.BigIntegerField(null=True, default=None)
    # 邮箱
    email = models.EmailField(max_length=254, null=True, default=None)
    # 密码
    pwd = models.CharField(max_length=40)


class Student(models.Model):
    # 工号
    workID = models.IntegerField(unique=True)
    # 姓名
    name = models.CharField(max_length=10)
    # 性别
    gender = models.IntegerField(choices=Gender.choices, null=True, default=None)
    # 手机号
    phoneNumber = models.BigIntegerField(null=True, default=None)
    # 邮箱
    email = models.EmailField(max_length=254, null=True, default=None)
    # 密码
    pwd = models.CharField(max_length=40)
    # 培训方案编号
    planID = models.IntegerField(null=True)
    # 考核编号
    requirementID = models.IntegerField(null=True)
    # 已修学分
    validCredit = models.IntegerField(null=True)


class Admin(models.Model):
    # 工号
    workID = models.IntegerField(unique=True)
    # 姓名
    name = models.CharField(max_length=10)
    # 性别
    gender = models.IntegerField(choices=Gender.choices, null=True, default=None)
    # 手机号
    phoneNumber = models.BigIntegerField(null=True, default=None)
    # 邮箱
    email = models.EmailField(max_length=254, null=True, default=None)
    # 密码
    pwd = models.CharField(max_length=40)


class Issues(models.Model):
    # 课程ID
    courseID = models.IntegerField()
    # 学员ID
    studentID = models.IntegerField()
    # 学员姓名
    studentName = models.CharField(max_length=10)
    # 标题
    title = models.CharField(max_length=50)
    # 描述
    description = models.TextField(max_length=300)
    # 状态
    status = models.IntegerField(choices=IssueStatus.choices)
    # 创建时间
    createTime = models.DateTimeField(auto_now_add=True)


class Discussion(models.Model):
    # IssueID
    issueID = models.IntegerField()
    # 发起者ID
    fromWhich = models.IntegerField()
    # 发起者身份
    fromWhat = models.IntegerField()
    # 发起者姓名
    fromWho = models.CharField(max_length=10)
    # 接收者ID
    toWhich = models.IntegerField(null=True)
    # 接收者身份
    toWhat = models.IntegerField(null=True)
    # 接收者姓名
    toWho = models.CharField(max_length=10, null=True)
    # 内容
    content = models.TextField(max_length=300)
    # 创建时间
    createTime = models.DateTimeField(auto_now_add=True)
