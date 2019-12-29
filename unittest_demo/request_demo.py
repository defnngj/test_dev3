import requests
import unittest


class AssertResultTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"

    def test_assert_result_method_error(self):
        data = {"result_text": "hello world",
                "assert_text": "hello",
                "assert_type": "include"}
        r = requests.get(self.base_url + "/case/assert_result/", data=data)
        print(r.status_code)
        print(r.json())
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["code"], 10100)
        self.assertEqual(result["message"], "请求方法错误")

    def test_assert_result_null(self):
        data = {"result_text": "",
                "assert_text": "",
                "assert_type": "include"}
        r = requests.post(self.base_url + "/case/assert_result/", data=data)
        print(r.status_code)
        print(r.json())
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["code"], 10101)
        self.assertEqual(result["message"], "断言的参数不能为空")

    def test_assert_result_type_error(self):
        data = {"result_text": "hello world",
                "assert_text": "hello",
                "assert_type": "abc"}
        r = requests.post(self.base_url + "/case/assert_result/", data=data)
        print(r.status_code)
        print(r.json())
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["code"], 10102)
        self.assertEqual(result["message"], "断言的类型错误")

    def test_assert_result_type_include(self):
        data = {"result_text": "hello world",
                "assert_text": "hello",
                "assert_type": "include"}
        r = requests.post(self.base_url + "/case/assert_result/", data=data)
        print(r.status_code)
        print(r.json())
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["code"], 10200)
        self.assertEqual(result["message"], "断言包含成功")

    def test_assert_result_type_include_error(self):
        data = {"result_text": "hello world",
                "assert_text": "hi",
                "assert_type": "include"}
        r = requests.post(self.base_url + "/case/assert_result/", data=data)
        print(r.status_code)
        print(r.json())
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["code"], 10200)
        self.assertEqual(result["message"], "断言包含失败")


if __name__ == '__main__':
    unittest.main()
