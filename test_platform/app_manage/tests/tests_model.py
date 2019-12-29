from django.test import TestCase
from app_manage.models import Project, Module


# django的测试不会读取数据库里面的数据，不会污染到数据库
class ProjectTest(TestCase):

    def setUp(self):
        Project.objects.create(name="first project",
                               describe="test case")

    def test_query_project(self):
        # 查询
        project = Project.objects.get(name="first project")
        self.assertEqual(project.describe, "test case")

    def test_add_project(self):
        # 添加
        Project.objects.create(name="project2", describe="this is project2")
        # 查询
        project = Project.objects.get(name="project2")
        self.assertEqual(project.describe, "this is project2")

    def test_update_project(self):
        # 更新
        project = Project.objects.get(name="first project")
        project.name = "project3"
        project.describe = "desc"
        project.save()
        project3 = Project.objects.get(name="project3")
        self.assertEqual(project3.describe, "desc")

    def test_delete_project(self):
        # 删除
        project = Project.objects.get(name="first project")
        project.delete()

        project = Project.objects.filter(name="first project")
        self.assertEqual(len(project), 0)



# 按照粒度运行测试
# python manage.py test app_manage
# python manage.py test app_manage.tests
# python manage.py test app_manage.tests.ProjectTest
# python manage.py test app_manage.tests.ProjectTest.test_de lete_project

