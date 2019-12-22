from django.db import models


class Variable(models.Model):
    """
    用户自定义变量表
    """
    key = models.CharField("名称", max_length=100, blank=False)
    value = models.CharField("值", max_length=500, blank=False)
    describe = models.TextField("描述", default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.key

