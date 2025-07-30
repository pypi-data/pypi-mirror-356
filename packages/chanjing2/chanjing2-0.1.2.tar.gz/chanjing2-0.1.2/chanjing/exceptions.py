class BaseException(Exception):
    """
    自定义基础异常类，支持错误消息、错误代码和参考URL
    """

    def __init__(
        self, msg="An error occurred", code="E000", reference_url=None, *args, **kwargs
    ):
        self.msg = msg
        self.code = code
        self.reference_url = reference_url
        self.details = kwargs.get("details", {})

        # 构建完整错误消息
        message = f"[{self.code}] {self.msg}"
        if self.reference_url:
            message += f" (参考: {self.reference_url})"

        super().__init__(message, *args)

    def to_dict(self):
        """返回异常的字典表示，方便转换为JSON"""
        result = {
            "error": {
                "code": self.code,
                "message": self.msg,
            }
        }

        if self.reference_url:
            result["error"]["reference_url"] = self.reference_url

        if self.details:
            result["error"]["details"] = self.details

        return result


class ChanjingException(BaseException):
    """禅境异常"""

    def __init__(
        self, msg="An error occurred", code="E000", reference_url=None, *args, **kwargs
    ):
        super().__init__(msg, code, reference_url, *args, **kwargs)
