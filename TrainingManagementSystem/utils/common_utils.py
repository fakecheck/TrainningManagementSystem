from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from ..errors.error import *


def bindParamsToModel(srcDict, model):
    """
    将请求参数转换成model
    :param srcDict: 请求参数， 一般是request.data
    :param model: 目标model
    :return: 新生成的 该model的object
    """
    _ = model()
    data = {}
    for _field in _._meta.fields:
        field = str(_field).split('.')[-1]
        if field != 'id' and field != "createTime" and field != "modifyTime":
            if field in srcDict:
                data[field] = srcDict[field]

    instance = model(**data)
    return instance


def bindParamsToDict(srcDict, keys, autoFilling=False, fillUsing=None):
    """
    将请求参数转换成字典
    :param srcDict: 请求参数，一般是request.data
    :param keys: 目标字段
    :param autoFilling: 未找到的目标字段是否自动填充
    :param fillUsing: 使用什么填充，默认为None，可以设置为空字符串等
    :return: 返回字典
    """
    data = {}
    for key in keys:
        if key in srcDict:
            data[key] = srcDict[key]
        elif autoFilling:
            data[key] = fillUsing
    return data


def updateModelUsingParam(srcDict, editable_keys, model, immutables=None):
    """
    使用请求参数更新model下的object
    :param srcDict: 请求参数，一般是request.data
    :param editable_keys: 可以编辑的字段（某些字段生成时必须指定并且不能修改）
    :param immutables: 设定后就没有办法修改的字段
    :param model: 目标model
    :return: 该model更新后的object
    """
    if immutables is None:
        immutables = []
    editable_keys.insert(0, 'id')
    data = bindParamsToDict(srcDict, editable_keys)
    objectId = data.get("id", -1)

    if objectId <= 0:
        return None, Response(NewError(TMSError.PARAM_ERROR, "id not provided or invalid"))

    try:
        object = model.objects.get(id=objectId)
    except ObjectDoesNotExist:
        return None, Response(NewError(TMSError.DO_NOT_EXIST))

    for key in editable_keys[1:]:
        tar = data.get(key, None)
        if tar is not None:
            if key not in immutables or object.__dict__[key] is None:
                object.__dict__[key] = tar
            else:
                return None, Response(NewError(TMSError.INVALID_OPERATION, "changing unalterable fields"))
    return object, None
