import os
import json
import unittest
import requests
import xmlrunner
from ddt import ddt, file_data
EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")


@ddt
class TaskTest(unittest.TestCase):

    @file_data(TASK_DATA)
    def test_file_data_json_dict_dict(self, url, method, header, parameter_type, parameter_body, assert_type, assert_text):

        header = json.loads(header)
        per_value = json.loads(parameter_body)

        if method == 1:
            r = requests.get(url, params=per_value, headers=header)
            if assert_type == 1:
                self.assertIn(assert_text, r.text)
            if assert_type == 2:
                self.assertEquals(assert_text, r.text)

        elif method == 2:
            if parameter_type == 1:
                r = requests.post(url, data=per_value, headers=header)
                if assert_type == 1:
                    self.assertIn(assert_text, r.text)
                if assert_type == 2:
                    self.assertEquals(assert_text, r.text)
            if parameter_type == 1:
                r = requests.post(url, json=per_value, headers=header)
                if assert_type == 1:
                    self.assertIn(assert_text, r.text)
                if assert_type == 2:
                    self.assertEquals(assert_text, r.text)


if __name__ == '__main__':
    with open(TASK_RESULTS, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
