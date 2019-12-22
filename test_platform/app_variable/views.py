from django.shortcuts import render
from app_variable.models import Variable
from test_platform.common import response


def variable_list(request):
    """
    变量例表
    :param request:
    :return:
    """
    variable = Variable.objects.all()
    return render(request, "variable/list.html",{
        "variable": variable
    })


def save_variable(request):
    """
    保存变量
    """
    if request.method == "POST":
        vid = request.POST.get("vid", "")
        key = request.POST.get("key", "")
        value = request.POST.get("value", "")
        desc = request.POST.get("desc", "")

        if key == "" or value == "":
            return response(10102, "必传参数为空")

        if vid == "0":
            Variable.objects.create(key=key, value=value, describe=desc)
            return response()
        else:
            variable = Variable.objects.get(id=vid)
            variable.key = key
            variable.value = value
            variable.describe = desc
            variable.save()
            return response()
    else:
        return response(10101, "请求方法错误")

'''
{
  "code": 10200, 
  "data": {
    "id": [
    {"name": "tom"},
    {"value": "abc"},
    ], 
    "name": "618\u62bd\u5956\u6d3b\u52a8"
  }, 
  "message": "success"
}
'''
"data.id.0.name"
"data.id.1.value"

# r["data"]['id'][0]['name']

