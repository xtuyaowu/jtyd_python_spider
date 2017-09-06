import flask

HTTP_SUCCESS = 200
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_ERROR = 500


class resumeParsinglog():
    resumeParsingwarning = "Have a wrong item parsing resume %s:%s,from platform:%s"

#发送请求错误
class BadRequestError(Exception):
    def __init__(self, msg_id ,email_id):
        self.error_code = None
        self.msg = None
        self.msg_id = msg_id
        self.email_id = email_id
    def __str__(self):
        return "%s(%s): %s" % (self.__class__.__name__, self.error_code, self.msg)
    def getvalue(self):
        return "%s(%s): %s" % (self.__class__.__name__, self.error_code, self.msg)


class MissingArgumentError(BadRequestError):
    def __init__(self, key):
        super(MissingArgumentError, self).__init__(HTTP_BAD_REQUEST, "%s is missing" % key)

class BadArgumentError(BadRequestError):
    def __init__(self, key, value):
        super(BadArgumentError, self).__init__(
            HTTP_BAD_REQUEST,
            "%s has wrong value(%s)" % (key, value)
        )





