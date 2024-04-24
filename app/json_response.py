# 统一json返回格式
class JsonResponse(object):
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def success(cls, code=200, msg='success', data=None):
        return cls(code, msg, data)

    @classmethod
    def fail(cls, code=400, msg='fail', data=None):
        return cls(code, msg, data)

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
