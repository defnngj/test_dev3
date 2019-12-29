from django.test import TestCase
from app_manage.models import Project, Module
from django.contrib.auth.models import User


class ProjectListTest(TestCase):

    def setUp(self):
        # 创建登录的用户数据
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        # 创建项目数据
        Project.objects.create(name="first project",describe="test case")

        # 执行登录
        login_user = {"username": "admin", "password": "admin123456"}
        resp = self.client.post("/login/", data=login_user)
        self.assertEqual(resp.status_code, 302)

    def test_project_manage_page(self):
        response = self.client.get("/manage/project_list/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"first project", response.content)


class ProjectAddTest(TestCase):

    def setUp(self):
        # 创建登录的用户数据
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        # 执行登录
        login_user = {"username": "admin", "password": "admin123456"}
        resp = self.client.post("/login/", data=login_user)
        self.assertEqual(resp.status_code, 302)

    def test_add_project(self):
        project_data = {"name": "项目AAA",
                        "describe": "这是个AAA 项目",
                        "status": True}

        resp = self.client.post("/manage/project_add/", data=project_data)
        print(resp.status_code)
        print(resp.content)
        project = Project.objects.get(name="项目AAA")
        self.assertEqual(project.describe, "这是个AAA 项目")
