import os
import json
from time import sleep
import threading
from xml.dom.minidom import parse
from app_case.models import TestCase
from app_task.models import TestTask
from app_task.models import TestResult
from app_task.setting import TASK_DATA, TASK_RESULTS, TASK_RUN


class TaskThread:

    def __init__(self, task_id):
        self.task_id = task_id

    def run_cases(self):
        # 1、获取任务下面用例id列表
        task = TestTask.objects.get(id=self.task_id)
        cases_list = task.cases[1:-1].split(",")
        task.status = 1
        task.save()

        # 2、通过用例ID 将用例写到 task_data.json文件里面
        cases_dict = {}
        for case in cases_list:
            case = TestCase.objects.get(id=case)
            print(case.name)
            cases_dict[case.name] = {
                "url": case.url,
                "method": case.method,
                "header": case.header,
                "parameter_type": case.parameter_type,
                "parameter_body": case.parameter_body,
                "assert_type": case.assert_type,
                "assert_text": case.assert_text,
            }

        cases_str = json.dumps(cases_dict)
        with open(TASK_DATA, "w") as f:
            f.write(cases_str)

        print("运行的任务文件：", TASK_RUN)

        # 3、运行测试任务
        os.system("python " + TASK_RUN)  # 耗时代码
        sleep(2)

        # 4、保存结果
        self.save_result()

        # 5、修改任务状态
        task = TestTask.objects.get(id=self.task_id)
        task.status = 2
        task.save()

    def save_result(self):
        """保存测试结果"""
        f = open(TASK_RESULTS, 'r', encoding='utf-8')
        xml_results = f.read()
        f.close()
        dom = parse(TASK_RESULTS)
        root = dom.documentElement
        test_suite = root.getElementsByTagName('testsuite')
        errors = test_suite[0].getAttribute("errors")
        failures = test_suite[0].getAttribute("failures")
        skipped = test_suite[0].getAttribute("skipped")
        name = test_suite[0].getAttribute("name")
        tests = test_suite[0].getAttribute("tests")
        time = test_suite[0].getAttribute("time")

        TestResult.objects.create(
            task_id=self.task_id,
            name=name,
            tests=tests,
            failures=failures,
            errors=errors,
            skipped=skipped,
            run_time=time,
            result=xml_results,
        )

    def run_tasks(self):
        print("创建线程任务...")
        sleep(2)
        t1 = threading.Thread(target=self.run_cases)
        t1.start()
        t1.join()

    def run(self):
        t = threading.Thread(target=self.run_tasks)
        t.start()
