# coding=utf-8
from .serializers import *
from .models import *
import datetime
from .customApiView import CAPIView
from django.db import IntegrityError
from rest_framework.renderers import JSONRenderer
from django_redis import get_redis_connection
from .utils.common_utils import *


# 注册 / 修改个人信息
# 注册 / 修改个人信息 - 管理员
class AdminRegisterAPI(CAPIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        admin = bindParamsToModel(request.data, Admin)
        try:
            admin.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))

        return Response()

    def put(self, request):
        # 可以编辑的数据
        editable_keys = ['gender', 'phoneNumber', 'email', 'pwd']

        # 设定后不能修改的数据
        immutables = ['gender']

        admin, resp = updateModelUsingParam(request.data,
                                            editable_keys, Admin, immutables=immutables)
        if resp is not None:
            return resp

        try:
            admin.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()


# 注册 / 修改个人信息 - 学员
class StudentRegisterAPI(CAPIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        error = None
        student, err = bindParamsToModel(request.data, Student)

        if student.planID is None:
            conn = get_redis_connection()
            defaultPlanID = conn.get("default_planID")
            if defaultPlanID is not None:
                student.planID = defaultPlanID
            else:
                error = NewError(TMSError.NOT_SET,
                                 "Your training plan is not set, please contact your admin and set it first, "
                                 "otherwise you cannot choose course")

        if student.requirementID is None:
            conn = get_redis_connection()
            requirement = conn.get("default_requirementID")
            if requirement is not None:
                student.requirementID = requirement
            else:
                error = NewError(TMSError.NOT_SET,
                                 "Your requirement is not set, please contact your admin and set it first, "
                                 "otherwise you cannot choose course")

        try:
            student.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response(error)

    def put(self, request):
        # 可以编辑的数据
        editable_keys = ['gender', 'phoneNumber', 'email', 'pwd', 'planID', 'requirementID']

        # 设定后不能修改的数据
        immutables = ['gender', 'planID', 'requirementID']
        student, resp = updateModelUsingParam(request.data,
                                              editable_keys, Student, immutables=immutables)
        if resp is not None:
            return resp

        try:
            student.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()


# 注册 / 修改个人信息 - 讲师
class TeacherRegisterAPI(CAPIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        teacher = bindParamsToModel(request.data, Teacher)

        try:
            teacher.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()

    def put(self, request):
        # 可以编辑的数据
        editable_keys = ['gender', 'phoneNumber', 'email', 'pwd']

        # 设定后不能修改的数据
        immutables = ['gender']
        teacher, resp = updateModelUsingParam(request.data,
                                              editable_keys, Teacher, immutables=immutables)
        if resp is not None:
            return resp

        try:
            teacher.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()


# 登录
# 登录 - 管理员
class AdminLoginAPI(CAPIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        keys = ['workID', 'pwd']
        data = bindParamsToDict(request.data, keys, autoFilling=True, fillUsing="")
        if data['workID'] == "" or data['pwd'] == "":
            return Response(NewError(TMSError.PARAM_ERROR, "require workID and password"))

        try:
            admin = Admin.objects.get(workID=data['workID'])
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST, "workID does not exist"))

        if data['pwd'] == admin.pwd:
            return Response()
        return Response(NewError(TMSError.ID_PWD_MISMATCH, "workID and pwd do not match"))


# 登录 - 教师
class TeacherLoginAPI(CAPIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        keys = ['workID', 'pwd']
        data = bindParamsToDict(request.data, keys, autoFilling=True, fillUsing="")
        if data['workID'] == "" or data['pwd'] == "":
            return Response(NewError(TMSError.PARAM_ERROR, "require workID and password"))

        try:
            teacher = Teacher.objects.get(workID=data['workID'])
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST, "workID does not exist"))

        if data['pwd'] == teacher.pwd:
            return Response()
        return Response(NewError(TMSError.ID_PWD_MISMATCH, "workID and pwd do not match"))


# 登录 - 学生
class StudentLoginAPI(CAPIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        keys = ['workID', 'pwd']
        data = bindParamsToDict(request.data, keys, autoFilling=True, fillUsing="")
        if data['workID'] == "" or data['pwd'] == "":
            return Response(NewError(TMSError.PARAM_ERROR, "require workID and password"))

        try:
            student = Student.objects.get(workID=data['workID'])
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST, "workID does not exist"))

        if data['pwd'] == student.pwd:
            return Response()
        return Response(NewError(TMSError.ID_PWD_MISMATCH, "workID and pwd do not match"))


# 培训方案管理
# 培训方案增删改查 - 管理员
class AdminPlanManagement(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        plans = TrainingPlans.objects.all()
        plansSerializer = PlanSerializer(plans, many=True)
        return Response(plansSerializer.data)

    def post(self, request):
        plan = bindParamsToModel(request.data, TrainingPlans)

        try:
            plan.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()

    def put(self, request):
        # 可以编辑的数据
        editable_keys = ['planName', 'description']

        plan, resp = updateModelUsingParam(request.data,
                                           editable_keys, TrainingPlans)
        if resp is not None:
            return resp

        try:
            plan.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()

    def delete(self, request):
        keys = ['id']
        data = bindParamsToDict(request.data, keys, autoFilling=True)
        if data['id'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "id cannot be empty"))
        id = data["id"]
        try:
            plan = TrainingPlans.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST))

        plan.delete()
        try:
            Student.objects.filter(planID=id).update(planID=None)
        except Exception as e:
            return Response(NewError(TMSError.DATABASE_ERROR, str(e)))
        return Response()


# 默认方案设定 - 管理员
class AdminPlanSetting(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        conn = get_redis_connection()
        defaultPlanID = conn.get("default_planID")
        if defaultPlanID is None:
            return Response(NewError(TMSError.NOT_SET, "default_planID not set yet"))

        return Response({"defaultPlanID": defaultPlanID})

    def post(self, request):
        keys = ['defaultPlanID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)
        if data['defaultPlanID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "defaultPlanID cannot be empty"))

        conn = get_redis_connection()
        conn.set("default_planID", data['defaultPlanID'], None)
        return Response()


# 学员培养方案修改 - 管理员
class AdminPlanAppoint(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        keys = ['workID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)
        if data['workID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "workID cannot be empty"))

        try:
            student = Student.obejcts.get(workID=data['workID'])
        except ObjectDoesNotExist as e:
            return Response(NewError(TMSError.DO_NOT_EXIST, str(e)))

        return Response({"planID": student.planID})

    def put(self, request):
        # 可以编辑的数据
        editable_keys = ['planID']
        student, resp = updateModelUsingParam(request.data,
                                              editable_keys, Student)
        if resp is not None:
            return resp

        try:
            student.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()


# 考核方案管理
# 考核方案增删改查 - 管理员
class AdminRequirementManagement(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        requirements = Requirement.objects.all()
        requirementSerializer = RequirementSerializer(requirements, many=True)
        return Response(requirementSerializer.data)

    def post(self, request):
        requirement = bindParamsToModel(request.data, Requirement)

        requirement.deadline = datetime.datetime.strptime(requirement.deadline, "%Y-%m-%d %H:00:00")
        if datetime.datetime.now() >= requirement.deadline:
            return Response(NewError(TMSError.PARAM_ERROR, "time {time} is in the past".format(
                time=requirement.deadline.strftime("%Y-%m-%d %H:%M:%S"))))

        try:
            requirement.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()

    def put(self, request):
        # 可以编辑的数据
        editable_keys = ['planName', 'requirement', 'deadline']

        requirement, resp = updateModelUsingParam(request.data,
                                                  editable_keys, Requirement)

        if resp is not None:
            return resp

        requirement.deadline = datetime.datetime.strptime(requirement.deadline, "%Y-%m-%d %H:00:00")
        if datetime.datetime.now() <= requirement.deadline:
            return Response(NewError(TMSError.PARAM_ERROR, "time {time} is in the past".format(
                time=requirement.deadline.strftime("%Y-%m-%d %H:%M:%S"))))

        try:
            requirement.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()

    def delete(self, request):
        keys = ['id']
        data = bindParamsToDict(request.data, keys, autoFilling=True)
        if data['id'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "id cannot be empty"))
        id = data["id"]
        try:
            requirement = Requirement.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST))

        requirement.delete()
        try:
            Student.objects.filter(planID=id).update(planID=None)
        except Exception as e:
            return Response(NewError(TMSError.DATABASE_ERROR, str(e)))
        return Response()


# 默认方案设定 - 管理员
class AdminRequirementSetting(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        conn = get_redis_connection()
        defaultPlanID = conn.get("default_requirementID")
        if defaultPlanID is None:
            return Response(NewError(TMSError.NOT_SET, "default_requirementID not set yet"))

        return Response({"defaultRequirementID": defaultPlanID})

    def post(self, request):
        keys = ['defaultRequirementID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)
        if data['defaultRequirementID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "defaultRequirementID cannot be empty"))

        conn = get_redis_connection()
        conn.set("default_requirementID", data['defaultRequirementID'], None)
        return Response()


# 学员考核方案修改 - 管理员
class AdminRequirementAppoint(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        keys = ['workID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)
        if data['workID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "workID cannot be empty"))

        try:
            student = Student.obejcts.get(workID=data['workID'])
        except ObjectDoesNotExist as e:
            return Response(NewError(TMSError.DO_NOT_EXIST, str(e)))

        return Response({"requirementID": student.requirementID})

    def put(self, request):
        # 可以编辑的数据
        editable_keys = ['requirementID']
        student, resp = updateModelUsingParam(request.data,
                                              editable_keys, Student)
        if resp is not None:
            return resp

        try:
            student.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()


# 课程管理
# 课程管理 - 管理员
class AdminCourseManagement(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        if request.data is None:
            courseInfos = CourseInfo.objects.all()
            infoSerializer = CourseInfoSerializer(courseInfos, many=True)
            return Response(infoSerializer.data)
        else:
            courseIDs = request.data['courseIDs']
            if not isinstance(courseIDs, list):
                return Response(TMSError.PARAM_ERROR, "courseIDs must be an list")
            if len(courseIDs) == 0:
                return Response()

            courseInfos = CourseInfo.objects.filter(id_in=courseIDs)
            infoSerializer = CourseInfoSerializer(courseInfos, many=True)
            res = []

            for courseinfo in infoSerializer.data:
                plans = [detail.planID for detail in
                         PlanDetailSerializer(PlanDetail.obejcts.filter(courseID=courseinfo.id),
                                              many=True).data]
                planNames = []
                for plan in plans:
                    trainingPlan = TrainingPlans.objects.filter(id=plan)
                    planName = trainingPlan[0].planName
                    planNames.append(planName)

                res.append({
                    "courseINFO": courseinfo,
                    "plans": plans,
                    "planNames": planNames,
                })
            return Response(res)

    def post(self, request):
        _ = CourseInfo()
        keys = [str(_field).split(".")[-1] for _field in _._meta.fields]
        keys.append("planIDs")
        data = bindParamsToDict(request.data, keys, autoFilling=True, fillUsing=None)

        # 课程状态系统自动维护
        data.pop("courseStatus")

        # 判定时间是否合法
        try:
            now = datetime.datetime.now()
            openFrom = data.get("openFrom", None)
            openUntil = data.get("openUntil", None)
            openFrom = datetime.datetime.strptime(openFrom, "%Y-%m-%d %H:00:00") if openFrom is not None else None
            openUntil = datetime.datetime.strptime(openUntil, "%Y-%m-%d %H:00:00") if openUntil is not None else None

            # 如果设定了结束时间但是没有设定开始时间
            # 默认从当前时间开始，到结束时间结束
            if openFrom is None and openUntil is not None:
                if openUntil > now:
                    data['openFrom'] = now.strftime("%Y-%m-%d %H:00:00")
                    data['courseStatus'] = CourseStatus.OPEN
                else:
                    return Response(NewError(TMSError.PARAM_ERROR, "course Open time invalid"))
            # 如果设定了开始时间，但是没有设定结束时间
            # 从开始时间开始，无限期开放
            elif openFrom is not None and openUntil is None:
                if openFrom > now:
                    data['courseStatus'] = CourseStatus.OPEN
                else:
                    return Response(NewError(TMSError.PARAM_ERROR, "course Open time invalid"))
            # 如果设定了开始时间和结束时间
            # 从开始时间开始，从结束时间结束
            elif openFrom is not None and openUntil is not None:
                if now < openFrom < openUntil:
                    data['courseStatus'] = CourseStatus.OPEN
                else:
                    return Response(NewError(TMSError.PARAM_ERROR, "course Open time invalid"))

        except Exception as e:
            return Response(NewError(TMSError.PARAM_ERROR, str(e)))

        # 判定planID是否合法
        if len(data['planIDs']) == 0:
            return Response(NewError(TMSError.PARAM_ERROR, "course must belong to at least one training plan"))

        for planID in data['planIDs']:
            if len(TrainingPlans.objects.filter(id=planID)) != 1:
                return Response(TMSError.PARAM_ERROR, "planID invalid")

        try:
            courseInfo = bindParamsToModel(data, CourseInfo)
            courseInfo.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))

        for planID in data['planIDs']:
            planDetail = PlanDetail(
                courseID=courseInfo.id,
                planID=planID
            )
            planDetail.save()

        return Response()

    def put(self, request):
        _ = CourseInfo()
        editable_keys = [str(_field).split(".")[-1] for _field in _._meta.fields]

        editable_keys.remove("createTime")
        editable_keys.remove("modifyTime")
        editable_keys.remove("courseStatus")

        course, resp = updateModelUsingParam(request.data,
                                             editable_keys, CourseInfo)
        if resp is not None:
            return resp

        # 判定时间是否合法
        now = datetime.datetime.now()
        openFrom = datetime.datetime.strptime(course.openFrom,
                                              "%Y-%m-%d %H:00:00") if course.openFrom is not None else None
        openUntil = datetime.datetime.strptime(course.openUntil,
                                               "%Y-%m-%d %H:00:00") if course.openUntil is not None else None

        if openFrom is None and openUntil is not None:
            if openUntil > now:
                course.openFrom = now.strftime("%Y-%m-%d %H:00:00")
                course.courseStatus = CourseStatus.OPEN
            else:
                return Response(NewError(TMSError.PARAM_ERROR, "course Open time invalid"))
        elif openFrom is not None and openUntil is None:
            if openFrom > now:
                course.courseStatus = CourseStatus.OPEN
            else:
                return Response(NewError(TMSError.PARAM_ERROR, "course Open time invalid"))
        elif openFrom is not None and openUntil is not None:
            if now < openFrom < openUntil:
                course.courseStatus = CourseStatus.OPEN
            else:
                return Response(NewError(TMSError.PARAM_ERROR, "course Open time invalid"))

        # 判断planID是否合法
        if request.data['planIDs'] is not None and len(request.data['planIDs']) != 0:
            for planID in request.data['planIDs']:
                if len(TrainingPlans.objects.filter(id=planID)) != 1:
                    return Response(TMSError.PARAM_ERROR, "planID invalid")
        try:
            course.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))

        # 修改课程plan归属关系
        if request.datap['planID'] is not None and len(request.data['planIDs']) != 0:
            curPlans = [plan.planID for plan in
                        PlanSerializer(PlanDetail.objects.filter(courseID=course.id), many=True).data]

            for planID in request.data['planIDs']:
                if planID not in curPlans:
                    planDetail = PlanDetail(
                        courseID=course.id,
                        planID=planID
                    )
                    planDetail.save()
            for planID in curPlans:
                if planID not in request.data['planIDs']:
                    planDetail = PlanDetail.objects.filter(courseID=course.id, planID=planID)
                    planDetail.delete()

        return Response()

    def delete(self, request):
        keys = ['courseID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)

        if data['courseID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "courseID cannot be empty"))

        courseInfo = CourseInfo.objects.filter(id=data['courseID'])
        if len(courseInfo) == 0:
            return Response(NewError(TMSError.DO_NOT_EXIST, "course does not exist"))

        # TODO 删除可能在上课的课程 需要进行可能的资源回收
        if courseInfo.courseStatus == CourseStatus.CLOSED:
            # 资源回收
            return Response()

        # 删除对应的培训方案中的课程
        for planDetail in PlanDetail.objects.filter(courseID=courseInfo.id):
            planDetail.delete()

        # 软删除
        try:
            courseInfo.courseStatus = CourseStatus.DELETED
            courseInfo.save()
        except Exception as e:
            return Response(NewError(TMSError.DATABASE_ERROR))

        return Response()


class StudentCourseList(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        keys = ['planID']
        data = bindParamsToDict(request.data, keys, autoFilling=True, fillUsing=None)
        if data['planID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "You must choose a plan before you can view course list"))

        courseIDs = [data.courseID for data in PlanDetail.objects.filter(planID=data['planID'])]
        courseInfos = CourseInfo.objects.filter(id_in=courseIDs)
        courseSerializer = CourseInfoSerializer(courseInfos, many=True)
        return Response(courseSerializer.data)

    def post(self, request):
        keys = ['workID', 'courseID', 'planID', 'requirementID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)

        if data['workID'] is None or data['courseID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "workID and courseID cannot be empty"))
        if data['planID'] is None or data['requirementID'] is None:
            return Response(
                NewError(TMSError.PARAM_ERROR, "You must have plan and requirement chosen before you choose course"))

        # 检查课程是否存在
        try:
            course = CourseInfo.objects.get(id=data['courseID'])
        except ObjectDoesNotExist as e:
            return Response(NewError(TMSError.DO_NOT_EXIST, "course do not exist"))

        # 检查课程是否合法
        try:
            plan = TrainingPlans.objects.get(id=data['planID'])
        except ObjectDoesNotExist as e:
            return Response(NewError(TMSError.DO_NOT_EXIST, "training plan do not exist"))
        planCourseList = [data.courseID for data in PlanDetail.objects.filter(planID=plan.id)]
        if data['courseID'] not in planCourseList:
            return Response(NewError(TMSError.DO_NOT_EXIST, "training plan do not include this course"))

        # 课程是否开放
        if course.courseStatus == CourseStatus.CLOSED:
            return Response(TMSError.CLOSED_COURSE, "course already closed")
        elif course.courseStatus == CourseStatus.NOT_AVAILABLE:
            return Response(TMSError.PARAM_ERROR, "course status invalid, contact admin")
        elif course.courseStatus == CourseStatus.DELETED:
            return Response(TMSError.PARAM_ERROR, "course already deleted, contact admin")
        elif course.courseStatus == CourseStatus.SETTLED:
            return Response(TMSError.PARAM_ERROR, "course already settled, contact admin")

        # 课程是否已经选择
        cts = CourseTaking.objects.filter(studentID=data['workID'], courseID=data['courseID'])
        if len(cts) != 0:
            return Response(NewError(TMSError.ALREADY_EXIST, "course already taken"))

        ct = bindParamsToModel(data, CourseTaking)
        ct.creditAward = course.creditAward if course.creditAward is not None else None
        try:
            ct.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))
        return Response()

    def delete(self, request):
        keys = ['workID', 'courseID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)

        if data['workID'] is None or data['courseID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "workID and ID cannot be empty"))

        ct = CourseTaking.objects.filter(studentID=data['workID'], courseID=data['courseID'])
        if len(ct) == 0:
            return Response(NewError(TMSError.DO_NOT_EXIST, "course not taken yet"))
        elif len(ct) != 1:
            return Response(NewError(TMSError.DATABASE_ERROR, "Please contact admin, something wrong with your record"))

        try:
            ct.delete()
        except Exception as e:
            return Response(NewError(TMSError.DATABASE_ERROR))

        return Response()


class StudentComment(CAPIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        keys = ['courseID', 'workID']
        data = bindParamsToDict(request.data, keys)

        if data['courseID'] is None or data['workID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "courseID and workID cannot be empty"))

        cts = CourseTaking.objects.filter(studentID=data['workID'], courseID=data['courseID'])
        if len(cts) == 0:
            return Response(NewError(TMSError.DO_NOT_EXIST, "You didn't have this class yet"))

        comment = bindParamsToModel(request.data, CourseComments)

        try:
            comment.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))

        return Response()


# TODO
class TeacherGrading(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        keys = ['courseID']
        data = bindParamsToDict(request.data, keys, autoFilling=True)

        if data['courseID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "require courseID"))

        students = CourseTaking.objects.filter(courseID=data['courseID']).value_list('studentID')


class CourseIssue(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        keys = ['courseID']
        data = bindParamsToDict(request.data, keys)

        if data['courseID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "courseID cannot be empty"))

        return Response(IssueSerializer(Issues.objects.filter(courseID=data['courseID']), many=True).data)

    def post(self, request):
        _ = Issues()
        keys = [str(_field).split(".")[-1] for _field in _._meta.fields]

        data = bindParamsToDict(request.data, keys)

        data.pop("status")
        data.pop("createTime")

        if data['courseID'] is None or data['studentID'] is None or data['studentName'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "courseID/studentID/studentName cannot be emtpy"))
        if data['title'] is None or data['description'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "title and description cannot be emtpy"))

        try:
            issue = bindParamsToModel(data, Issues)
            issue.status = IssueStatus.OPEN
            issue.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))

        return Response()

    def put(self, request):
        keys = ['workID', 'pwd', 'issueID']
        data = bindParamsToDict(request.data, keys)
        if data['workID'] is None or data['pwd'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "workID/pwd cannot be empty, please login again"))

        if data['issueID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "issueID cannot be empty"))

        teacher = Teacher.objects.filter(workID=data['workID'], pwd=data['pwd'])
        if len(teacher) == 0:
            return Response(NewError(TMSError.ID_PWD_MISMATCH, "workID and pwd do not match, please login again"))

        try:
            issue = Issues.objects.get(id=data['issueID'])
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST, "issue does not exist"))

        issue.status = IssueStatus.CLOSED

        try:
            issue.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))

        return Response()


class CourseDiscussion(CAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        keys = ['issueID']
        data = bindParamsToDict(request.data, keys)

        # issue存在且合法
        if data['issueID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "issueID cannot be empty"))

        try:
            issue = Issues.objects.get(id=data['issueID'])
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST, "issue does not exist"))

        return Response(DiscussionSerializer(Discussion.objects.filter(issueID=data['issueID']), many=True).data)

    def post(self, request):
        keys = ['issueID']
        data = bindParamsToDict(request.data, keys)

        # issue存在且合法
        if data['issueID'] is None:
            return Response(NewError(TMSError.PARAM_ERROR, "issueID cannot be empty"))

        try:
            issue = Issues.objects.get(id=data['issueID'])
        except ObjectDoesNotExist:
            return Response(NewError(TMSError.DO_NOT_EXIST, "issue does not exist"))

        # issue是开启状态
        if issue.status == IssueStatus.CLOSED:
            return Response(NewError(TMSError.INVALID_OPERATION, "issue already closed"))

        discussion = bindParamsToModel(request.data, Discussion)

        try:
            discussion.save()
        except IntegrityError as e:
            return Response(NewError(TMSError.INTEGRITY_ERROR, str(e)))
        except ValueError as e:
            return Response(NewError(TMSError.VALUE_ERROR, str(e)))

        return Response()
