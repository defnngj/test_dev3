from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# 用来写请求的处理逻辑
def hello(request):
    return render(request, "hello.html")


# django的处理过程：
# 1、url指定路径 /hello/
# 2、setting.py 找到url的配置文件。
# 3、urls.py匹配路径 /hello/ ，把请求指到 views 文件
# 4、再views.py 写 Response 的处理， 把 templates/ 目录下面的HTML文件，返回给客户端
