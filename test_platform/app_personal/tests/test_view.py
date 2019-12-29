from django.test import TestCase
from app_manage.models import Project, Module
from django.contrib.auth.models import User


class LoginTest(TestCase):

    def setUp(self):
        # 创建登录的用户数据
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_get_login_page(self):
        resp = self.client.get("/login/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "login.html")

    def test_login_null(self):
        # 执行登录
        login_user = {"username": "", "password": ""}
        resp = self.client.post("/login/", data=login_user)
        self.assertEqual(resp.status_code, 200)
        resp_str = resp.content.decode("utf-8")
        self.assertIn("用户名或密码为空", resp_str)

    def test_login_error(self):
        # 执行登录
        login_user = {"username": "user1", "password": "123456"}
        resp = self.client.post("/login/", data=login_user)
        self.assertEqual(resp.status_code, 200)
        resp_str = resp.content.decode("utf-8")
        self.assertIn("用户名或密码错误", resp_str)

    def test_login_success(self):
        # 执行登录
        login_user = {"username": "admin", "password": "admin123456"}
        resp = self.client.post("/login/", data=login_user)
        self.assertEqual(resp.status_code, 302)

