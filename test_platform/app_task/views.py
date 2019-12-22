from django.shortcuts import render
from django.http import HttpResponseRedirect
from test_platform.common import response
from app_manage.models import Project
from app_manage.models import Module
from app_case.models import TestCase
from app_task.models import TestTask
from app_task.models import TestResult
from app_task.extend.task_thread import TaskThread


def task_list(request):
    """
    任务列表
    """
    test_task = TestTask.objects.all()
    return render(request, "task/list.html",{
        "tasks": test_task
    })


def task_add(request):
    """
    创建任务页面
    """
    return render(request, "task/add.html")


def task_edit(request, tid):
    """
    编辑任务页面
    """
    return render(request, "task/edit.html")


def case_node(request):
    """用例的树形节点"""
    if request.method == "GET":
        data = []
        project = Project.objects.all()

        for p in project:
            project_dict = {
                "name": p.name,
                "isParent": True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in module:
                module_dict = {
                    "name": m.name,
                    "isParent": True
                }
                case = TestCase.objects.filter(module_id=m.id)
                case_list = []
                for c in case:
                    case_dict = {
                        "id": c.id,
                        "name": c.name,
                        "isParent": False,
                    }
                    case_list.append(case_dict)
                module_dict["children"] = case_list
                module_list.append(module_dict)
            project_dict["children"] = module_list
            data.append(project_dict)

        return response(10200, "success", data)

    elif request.method == "POST":
        task_id = request.POST.get("tid", "")
        task = TestTask.objects.get(id=task_id)
        case_list = task.cases[1:-1].split(",")
        case_list_int = []
        for c in case_list:
            case_list_int.append(int(c))

        task_data = {
            "taskName": task.name,
            "taskDesc": task.describe,
        }

        data = []
        project = Project.objects.all()

        for p in project:
            project_dict = {
                "name": p.name,
                "isParent": True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in module:
                module_dict = {
                    "name": m.name,
                    "isParent": True
                }
                case = TestCase.objects.filter(module_id=m.id)
                case_list = []
                for c in case:
                    print("", c.id, type(c.id))
                    if c.id in case_list_int:
                        case_dict = {
                            "id": c.id,
                            "name": c.name,
                            "isParent": False,
                            "checked": True
                        }
                    else:
                        case_dict = {
                            "id": c.id,
                            "name": c.name,
                            "isParent": False,
                            "checked": False
                        }
                    case_list.append(case_dict)
                module_dict["children"] = case_list
                module_list.append(module_dict)
            project_dict["children"] = module_list
            data.append(project_dict)

        task_data["data"] = data
        return response(10200, "success", task_data)

    else:
        return response(10100, "请求方法错误")


def task_save(request):
    """保存任务"""
    if request.method == "POST":
        task_id = request.POST.get("tid", "")
        task_name = request.POST.get("name", "")
        task_desc = request.POST.get("desc", "")
        task_cases = request.POST.get("cases", "")
        if task_name == "":
            return response(10102, "任务的名称为空")

        print("task_id", task_id, type(task_id))
        if task_id == "0":
            TestTask.objects.create(name=task_name,
                                    describe=task_desc,
                                    cases=task_cases)
        else:
            task = TestTask.objects.get(id=task_id)
            task.name = task_name
            task.describe = task_desc
            task.cases = task_cases
            task.save()
        return response()
    else:
        return response(10101, "请求方法错误")


def task_rung(request, tid):
    """运行任务"""
    task = TaskThread(tid)
    task.run()
    return HttpResponseRedirect("/task/")


def log_list(request, tid):
    """
    获取某一任务的历史结果
    """
    result = TestResult.objects.filter(task_id=tid)
    return render(request, "task/logs.html", {"result": result})


def get_log(request):
    """
    获取某一任务的历史结果
    """
    if request.method == "POST":
        rid = request.POST.get("rid", "")
        result = TestResult.objects.get(id=rid)
        return response(data=result.result)
    else:
        return response(10101, "请求方法错误")
