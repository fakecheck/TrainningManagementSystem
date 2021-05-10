class TMSError:
    PARAM_ERROR = 1
    INTEGRITY_ERROR = 2
    VALUE_ERROR = 3
    INVALID_OPERATION = 4
    DO_NOT_EXIST = 5
    ID_PWD_MISMATCH = 6
    DATABASE_ERROR = 7
    NOT_SET = 8
    CLOSED_COURSE = 9
    ALREADY_EXIST = 10


errMAP = {
    1: "PARAM_ERROR",
    2: "INTEGRITY_ERROR",
    3: "VALUE_ERROR",
    4: "INVALID_OPERATION",
    5: "DO_NOT_EXIST",
    6: "ID_PWD_MISMATCH",
    7: "DATABASE_ERROR",
    8: "NOT_SET",
    9: "CLOSED_COURSE",
    10: "ALREADY_EXIST"
}


def NewError(errcode, errMsg=None):
    data = {
        "errcode": errcode,
        "errType": errMAP[errcode],
        "errMsg": None
    }
    if errMsg is not None:
        data["errMsg"] = errMsg
    return data
