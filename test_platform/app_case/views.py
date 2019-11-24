import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from app_manage.models import Project, Module
from app_case.models import TestCase


def list_case(request):
    return render(request, "case/debug.html")


def send_req(request):
    """
    发送接口
    """
    if request.method == "GET":
        url = request.GET.get("url", "")
        method = request.GET.get("method", "")
        header = request.GET.get("header", "")
        per_type = request.GET.get("per_type", "")
        per_value = request.GET.get("per_value", "")

        print("url--->", url, type(url))
        print("header--->", header, type(header))
        print("method--->", method, type(method))
        print("per_type--->", per_type, type(per_type))
        print("per_value--->", per_value, type(per_value))
        if url == "":
            return JsonResponse({"code": 10101, "message": "URL不能为空！"})

        try:
            header = json.loads(header)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10102, "message": "Header格式错误，必须是标准的JSON格式！"})

        try:
            per_value = json.loads(per_value)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10103,
             "message": "参数格式错误，必须是标准的JSON格式！"})

        
        
        

        if method == "get":
            r = requests.get(url, params=per_value, headers=header)
        
        if method == "post":
            print("post")
            if per_type == "form":
                r = requests.post(url, data=per_value, headers=header)
            
            if per_type == "json":
                r = requests.post(url, json=per_value, headers=header)
            

        return JsonResponse({"code": 10200, "message":"success", "data": r.text})


def assert_result(request):
    """
    断言结果
    """
    if request.method == "POST":
        result_text = request.POST.get("result_text", "")
        assert_text = request.POST.get("assert_text", "")
        assert_type = request.POST.get("assert_type", "")

        if result_text == "" or assert_text == "":
            return JsonResponse({"code": 10101, "message": "断言的参数不能为空"})
        
        if assert_type != "include" and assert_type != "equal":
            return JsonResponse({"code": 10101, "message": "断言的参数不能为空"})

        if assert_type == "include":
            if assert_text in result_text:
                return JsonResponse({"code": 10200, "message": "断言包含成功"})
            else:
                return JsonResponse({"code": 10200, "message": "断言包含失败"})
        
        if assert_type == "equal":
            if assert_text == result_text:
                return JsonResponse({"code": 10200, "message": "断言相等成功"})
            else:
                return JsonResponse({"code": 10200, "message": "断言相等失败"})

        return JsonResponse({"code": 10102, "message": "fail"})


def get_select_data(request):
    """
    获取select下拉框需要项目/模块数据
    """
    if request.method == "GET":
        projects = Project.objects.all()
        data_list = []
        for p in projects:
            project_dict = {
                "id": p.id,
                "name": p.name
            }
            modules = Module.objects.filter(project=p)
            module_list = []
            for m in modules:
                module_dict = {
                    "id": m.id,
                    "name": m.name
                }
                module_list.append(module_dict)
            project_dict["moduleList"] = module_list
            data_list.append(project_dict)
        return JsonResponse({"code": 10200, "message":"success", "data": data_list})


def save_case(request):
    """
    保存用例
    """
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        per_type = request.POST.get("per_type", "")
        per_value = request.POST.get("per_value", "")
        result_text = request.POST.get("result_text", "")
        assert_text = request.POST.get("assert_text", "")
        assert_type = request.POST.get("assert_type", "")
        module_id = request.POST.get("module_id", "")
        case_name = request.POST.get("case_name", "")

        if method == "get":
            method_int = 1
        elif method == "post":
            method_int = 2
        else:
            return JsonResponse({"code": 10101, "message": "请求方法错误"})
        
        if per_type == "form":
            per_type_int = 1
        elif per_type == "json":
            per_type_int = 2
        else:
            return JsonResponse({"code": 10102, "message": "参数类型错误"})
        
        if assert_type == "include":
            assert_type_int = 1
        elif assert_type == "equal":
            assert_type_int = 2
        else:
            return JsonResponse({"code": 10103, "message": "参数类型错误"})

        TestCase.objects.create(module_id=module_id,
                                name=case_name,
                                method=method_int,
                                header=header,
                                parameter_type=per_type_int,
                                parameter_body=per_value,
                                result=result_text,
                                assert_text=assert_text,
                                assert_type=assert_type_int,                    
        )

        return JsonResponse({"code": 10200, "message":"save success"})
